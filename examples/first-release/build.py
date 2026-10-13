#!/usr/bin/env python3
"""Build an auditable, intentionally imperfect toy dataset using only Python."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

LABELS = ("access", "billing", "technical")
DEFAULT_SEED = "first-release-v1"
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}\Z")
RULES = (
    ("billing_terms", "billing", r"\b(invoice|refund|charge|payment)\b"),
    ("access_terms", "access", r"\b(password|login|locked)\b"),
    ("failure_terms", "technical", r"\b(crash|crashes|error|frozen)\b"),
)
REQUIRED_FIELDS = {"id", "source_id", "family_id", "text"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def jsonl_bytes(rows):
    return b"".join((json.dumps(row, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":"), allow_nan=False) + "\n")
                    .encode("utf-8") for row in rows)


def normalize(text):
    """NFKC, casefold, NFKC again, then collapse whitespace; retain punctuation."""
    folded = unicodedata.normalize("NFKC", text).casefold()
    # Case folding can introduce decomposed marks; finish in one canonical form.
    return " ".join(unicodedata.normalize("NFKC", folded).split())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number: " + value)


def strict_json(text):
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def valid_id(value):
    return isinstance(value, str) and ID_PATTERN.fullmatch(value) is not None


def read_records(data):
    """Quarantine each bad physical line; never silently repair or discard it."""
    accepted, quarantine, counts = [], [], {}
    for line_number, raw in enumerate(data.splitlines(keepends=True), 1):
        provenance = {
            "source_line": line_number,
            "raw_line_sha256": sha256(raw),
            "raw_line_base64": base64.b64encode(raw).decode("ascii"),
        }
        try:
            decoded = raw.decode("utf-8")
            row = strict_json(decoded)
            if not isinstance(row, dict):
                raise ValueError("record must be a JSON object")
            # Reserve an unambiguous ID even when another field is invalid.
            # A malformed duplicate must not let its valid twin survive.
            if valid_id(row.get("id")):
                counts[row["id"]] = counts.get(row["id"], 0) + 1
            if set(row) != REQUIRED_FIELDS:
                raise ValueError("fields must be exactly: family_id, id, source_id, text")
            for field in ("id", "source_id", "family_id"):
                if not valid_id(row[field]):
                    raise ValueError(field + " must be a nonempty ASCII identifier")
            if not isinstance(row["text"], str):
                raise ValueError("text must be a string")
            # Escaped unpaired surrogate code points are not valid UTF-8 text.
            raw_text_bytes = row["text"].encode("utf-8")
            normalized = normalize(row["text"])
            if not normalized:
                raise ValueError("text must not normalize to an empty string")
            accepted.append({**row, **provenance, "normalized_text": normalized,
                             "raw_text_sha256": sha256(raw_text_bytes)})
        except (ValueError, UnicodeError) as exc:
            quarantine.append({**provenance, "reason": str(exc)})
    # Quarantine ALL occurrences of a reused ID; picking a first row is order-dependent.
    unique = []
    for row in accepted:
        if counts[row["id"]] > 1:
            quarantine.append({key: row[key] for key in (
                "source_line", "raw_line_sha256", "raw_line_base64")}
                | {"reason": "duplicate record id: " + row["id"]})
        else:
            unique.append(row)
    return sorted(unique, key=lambda row: row["id"]), sorted(
        quarantine, key=lambda row: row["source_line"])


class UnionFind:
    def __init__(self, ids):
        self.parent = {item: item for item in ids}

    def find(self, item):
        while item != self.parent[item]:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left != right:
            self.parent[max(left, right)] = min(left, right)


def weak_label(text):
    votes = {name: label if re.search(pattern, text) else None
             for name, label, pattern in RULES}
    labels = {label for label in votes.values() if label is not None}
    if len(labels) == 1:
        return votes, next(iter(labels)), "labeled"
    return votes, None, "conflict" if labels else "abstain"


def prepare_release(rows, seed):
    """No gold argument: graph construction, splitting and votes cannot use gold."""
    graph = UnionFind(row["id"] for row in rows)
    first = {field: {} for field in ("source_id", "family_id", "canonical_id")}
    by_canonical = {}
    for row in rows:
        canonical_id = "ex-" + sha256(row["normalized_text"].encode("utf-8"))
        row["canonical_id"] = canonical_id
        by_canonical.setdefault(canonical_id, []).append(row)
        # One union graph includes ALL equality relations before any split happens.
        for field, seen in first.items():
            value = row[field]
            if value in seen:
                graph.union(row["id"], seen[value])
            else:
                seen[value] = row["id"]
    components = {}
    for row in rows:
        components.setdefault(graph.find(row["id"]), set()).add(row["canonical_id"])
    group_for_root = {
        root: "group-" + sha256("\n".join(sorted(ids)).encode("utf-8"))
        for root, ids in components.items()
    }
    groups = sorted(group_for_root.values(), key=lambda group: (
        sha256((seed + "\n" + group).encode("utf-8")), group))
    if len(groups) < 3:
        raise ValueError("need at least 3 leakage groups for nonempty train/dev/test")
    train_count = max(1, len(groups) * 60 // 100)
    dev_count = max(1, len(groups) * 20 // 100)
    split_for_group = {
        group: "train" if index < train_count else
        "dev" if index < train_count + dev_count else "test"
        for index, group in enumerate(groups)
    }
    release, lineage = [], []
    for canonical_id, originals in sorted(by_canonical.items()):
        representative = originals[0]
        group_id = group_for_root[graph.find(representative["id"])]
        split = split_for_group[group_id]
        votes, prediction, status = weak_label(representative["normalized_text"])
        release.append({"canonical_id": canonical_id, "text": representative["normalized_text"],
                        "group_id": group_id, "split": split, "rule_votes": votes,
                        "weak_label": prediction, "label_status": status})
        for row in originals:
            lineage.append({"record_id": row["id"], "source_id": row["source_id"],
                            "family_id": row["family_id"], "canonical_id": canonical_id,
                            "group_id": group_id, "split": split, "raw_text": row["text"],
                            **{key: row[key] for key in ("raw_text_sha256", "source_line",
                               "raw_line_sha256", "raw_line_base64")}})
    return release, sorted(lineage, key=lambda row: row["record_id"])


def read_gold(data, accepted_ids):
    gold = strict_json(data.decode("utf-8"))
    if not isinstance(gold, dict) or set(gold) != {"labels", "provenance"}:
        raise ValueError("gold must contain exactly labels and provenance")
    if not isinstance(gold["provenance"], str) or not gold["provenance"].strip():
        raise ValueError("gold provenance must be a nonempty string")
    labels = gold["labels"]
    if not isinstance(labels, dict):
        raise ValueError("gold labels must be an object mapping record IDs to labels")
    for record_id, label in labels.items():
        if record_id not in accepted_ids:
            raise ValueError("gold references unknown or quarantined record id: " + record_id)
        if not isinstance(label, str) or label not in LABELS:
            raise ValueError("invalid gold label for " + record_id)
    return labels


def accuracy(predictions, gold):
    evaluated = [(identifier, prediction) for identifier, prediction in predictions.items()
                 if prediction is not None and identifier in gold]
    correct = sum(prediction == gold[identifier] for identifier, prediction in evaluated)
    return {"correct": correct, "evaluated_predictions": len(evaluated),
            "accuracy": correct / len(evaluated) if evaluated else None}


def audit_release(rows, release, lineage, quarantine, gold):
    gold_by_canonical = {}
    for row in lineage:
        if row["record_id"] in gold:
            gold_by_canonical.setdefault(row["canonical_id"], []).append(
                {"record_id": row["record_id"], "label": gold[row["record_id"]]})
    resolved_gold, conflicts = {}, []
    for canonical_id, annotations in sorted(gold_by_canonical.items()):
        labels = {annotation["label"] for annotation in annotations}
        if len(labels) == 1:
            resolved_gold[canonical_id] = next(iter(labels))
        else:
            conflicts.append({"canonical_id": canonical_id, "annotations": annotations})
    total = len(release)
    rule_metrics = {}
    for name, label, pattern in RULES:
        predictions = {row["canonical_id"]: row["rule_votes"][name] for row in release}
        votes = sum(value is not None for value in predictions.values())
        rule_metrics[name] = {"label": label, "regex": pattern,
                              "coverage": {"voted_examples": votes, "eligible_examples": total,
                                           "coverage": votes / total if total else None},
                              **accuracy(predictions, resolved_gold)}
    predictions = {row["canonical_id"]: row["weak_label"] for row in release}
    errors = [{"canonical_id": identifier, "prediction": prediction,
               "gold": resolved_gold[identifier]} for identifier, prediction in sorted(predictions.items())
              if prediction is not None and identifier in resolved_gold
              and prediction != resolved_gold[identifier]]
    return {
        "caveat": "Tiny authored teaching fixture; these are descriptive checks, not evidence of generalization. "
                  "Rules are fixed heuristics, not a learned label model. Gold is evaluation-only. "
                  "Aggregate accuracy excludes aggregate abstentions/conflicts. Per-rule accuracy scores each rule\'s "
                  "non-abstaining votes. All accuracy denominators exclude unresolved/missing gold; inspect them.",
        "counts": {"input_lines": len(rows) + len(quarantine), "accepted_raw_records": len(rows),
                   "quarantined_lines": len(quarantine), "canonical_examples": total,
                   "duplicate_records_collapsed": len(rows) - total,
                   "leakage_groups": len({row["group_id"] for row in release})},
        "gold": {"annotated_raw_records": len(gold), "resolved_canonical_examples": len(resolved_gold),
                 "missing_canonical_examples": total - len(gold_by_canonical),
                 "conflicting_canonical_examples": len(conflicts), "conflicts": conflicts},
        "per_rule": rule_metrics,
        "weak_labels": {"labeled": sum(row["label_status"] == "labeled" for row in release),
                        "abstain": sum(row["label_status"] == "abstain" for row in release),
                        "conflict": sum(row["label_status"] == "conflict" for row in release),
                        **accuracy(predictions, resolved_gold), "errors": errors},
        "splits": {split: {"canonical_examples": sum(row["split"] == split for row in release),
                           "leakage_groups": len({row["group_id"] for row in release if row["split"] == split}),
                           **accuracy({row["canonical_id"]: row["weak_label"] for row in release
                                       if row["split"] == split}, resolved_gold)}
                   for split in ("train", "dev", "test")},
    }


def build(records_path, gold_path, out, seed=DEFAULT_SEED):
    records_path, gold_path, out = Path(records_path), Path(gold_path), Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("output must be a nonexistent or empty directory")
    raw_records, raw_gold = records_path.read_bytes(), gold_path.read_bytes()
    rows, quarantine = read_records(raw_records)
    release, lineage = prepare_release(rows, seed)
    # Gold enters only after release examples, component memberships and splits are fixed.
    gold = read_gold(raw_gold, {row["id"] for row in rows})
    audit = audit_release(rows, release, lineage, quarantine, gold)
    recipe = {
        "version": 3, "seed": seed, "labels": list(LABELS),
        "record_id_policy": "all strictly decoded objects with a valid unambiguous id reserve that identity; "
                            "quarantine every accepted occurrence of a reused id even if another occurrence is invalid; "
                            "undecodable lines and duplicate-key objects have no safely identifiable id",
        "normalization": "Unicode NFKC, casefold, NFKC again, collapse all Unicode whitespace, strip; retain punctuation",
        "unicode_database_version": unicodedata.unidata_version,
        "dedup": "exact equality of normalized text; SHA-256 canonical IDs; all raw lineage retained",
        "grouping": "connected components of equal canonical_id OR equal source_id OR equal family_id; global IDs",
        "splitting": "sort groups by SHA-256(seed + newline + group_id); floor(60%)/floor(20%)/remainder; "
                     "train and dev each at least one group; at least three groups required; no stratification",
        "weak_labeling": "fixed regex votes; unanimous non-abstaining class wins; conflicts and no votes abstain",
        "rules": [{"name": name, "label": label, "regex": pattern} for name, label, pattern in RULES],
        "gold_policy": "evaluation only; unknown IDs fail; missing allowed; conflicting duplicate annotations excluded",
        "serialization": "UTF-8, sorted object keys, LF endings; no clock or absolute path fields",
    }
    outputs = {
        "raw/records.jsonl": raw_records,
        "reference/gold.json": raw_gold,
        "release.jsonl": jsonl_bytes(release), "lineage.jsonl": jsonl_bytes(lineage),
        "quarantine.jsonl": jsonl_bytes(quarantine), "audit.json": json_bytes(audit),
        **{split + ".jsonl": jsonl_bytes([row for row in release if row["split"] == split])
           for split in ("train", "dev", "test")},
    }
    manifest = {
        "format_version": 1, "recipe": recipe, "recipe_sha256": sha256(json_bytes(recipe)),
        "inputs": {"records.jsonl": {"sha256": sha256(raw_records), "bytes": len(raw_records)},
                   "gold.json": {"sha256": sha256(raw_gold), "bytes": len(raw_gold)},
                   "build.py": {"sha256": sha256(Path(__file__).read_bytes())}},
        "outputs": {name: {"sha256": sha256(content), "bytes": len(content)}
                    for name, content in sorted(outputs.items())},
        "manifest_hash_policy": "manifest.json is excluded from its own output hash map to avoid recursion",
    }
    # No writes until validation and generation succeed. Never overwrite an existing release.
    out.mkdir(parents=True, exist_ok=True)
    for name, content in sorted(outputs.items()):
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(content)
    with (out / "manifest.json").open("xb") as handle:
        handle.write(json_bytes(manifest))
    return audit


def main(argv=None):
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=here / "data" / "records.jsonl")
    parser.add_argument("--gold", type=Path, default=here / "data" / "gold.json")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", default=DEFAULT_SEED)
    args = parser.parse_args(argv)
    try:
        audit = build(args.records, args.gold, args.out, args.seed)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, "build failed: " + str(exc) + "\n")
    print(json.dumps({"counts": audit["counts"], "weak_labels": audit["weak_labels"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
