"""CPU-only integration and regression tests for the first-release teaching lab."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

# Import the runnable example without adding a package or writing cache files.
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "first-release"
SPEC = importlib.util.spec_from_file_location("first_release", LAB / "build.py")
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class FirstReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def build_fixture(self, name="release", **kwargs):
        out = self.work / name
        lab.build(kwargs.pop("records", LAB / "data" / "records.jsonl"),
                  kwargs.pop("gold", LAB / "data" / "gold.json"), out, **kwargs)
        return out

    def write_inputs(self, records, gold=None):
        record_path = self.work / "records.jsonl"
        record_path.write_bytes(lab.jsonl_bytes(records))
        gold_path = self.work / "gold.json"
        gold_path.write_bytes(lab.json_bytes({"provenance": "Test-only handwritten labels.",
                                            "labels": gold or {}}))
        return record_path, gold_path

    @staticmethod
    def record(identifier, text, source=None, family=None):
        return {"id": identifier, "source_id": source or "src-" + identifier,
                "family_id": family or "family-" + identifier, "text": text}

    def test_fixture_counts_and_intentional_failures(self):
        out = self.build_fixture()
        audit = json.loads((out / "audit.json").read_text())
        self.assertEqual(audit["counts"], {"input_lines": 30, "accepted_raw_records": 28,
                         "quarantined_lines": 2, "canonical_examples": 24,
                         "duplicate_records_collapsed": 4, "leakage_groups": 21})
        weak = audit["weak_labels"]
        self.assertEqual((weak["labeled"], weak["abstain"], weak["conflict"]), (14, 5, 5))
        self.assertEqual((weak["correct"], weak["evaluated_predictions"]), (10, 13))
        self.assertEqual(len(weak["errors"]), 3)
        self.assertEqual(audit["gold"]["conflicting_canonical_examples"], 1)
        self.assertEqual(audit["gold"]["missing_canonical_examples"], 2)
        self.assertIn("Tiny authored teaching fixture", audit["caveat"])
        self.assertEqual((out / "audit.json").read_bytes(), (LAB / "expected" / "audit.json").read_bytes())
        expected = {"billing_terms": (9, 4, 8), "access_terms": (7, 4, 7),
                    "failure_terms": (8, 7, 8)}
        for name, (votes, correct, evaluated) in expected.items():
            metrics = audit["per_rule"][name]
            self.assertEqual((metrics["coverage"]["voted_examples"], metrics["correct"],
                              metrics["evaluated_predictions"]), (votes, correct, evaluated))

    def test_normalization_is_explicit_and_idempotent(self):
        self.assertEqual(lab.normalize("  ＩＮＶＯＩＣＥ\tStraße\nCafe\u0301\u00a0"), "invoice strasse café")
        self.assertEqual(lab.normalize("No refund!"), "no refund!")
        self.assertNotEqual(lab.normalize("refund?"), lab.normalize("refund!"))
        value = lab.normalize(" Ｐａｙｍｅｎｔ \tRECEIPT ")
        self.assertEqual(lab.normalize(value), value)

    def test_greek_combining_marks_are_case_equivalent_and_idempotent(self):
        spellings = ("\u0399\u0344", "\u03b9\u0344", "\u0399\u0308\u0301",
                     "\u03ca\u0301", "\u03b9\u0308\u0301", "\u0390")
        for spelling in spellings:
            with self.subTest(spelling=repr(spelling)):
                normalized = lab.normalize(spelling)
                self.assertEqual(normalized, "\u0390")
                self.assertEqual(lab.normalize(normalized), normalized)

    def test_greek_canonical_equivalence_unions_related_families_before_split(self):
        examples = [self.record("a", "\u0399\u0344", family="first-family"),
                    self.record("b", "\u03b9\u0308\u0301", family="second-family"),
                    self.record("c", "Related alternate wording", family="second-family"),
                    self.record("d", "Independent alpha"), self.record("e", "Independent beta")]
        accepted, quarantine = lab.read_records(lab.jsonl_bytes(examples))
        self.assertEqual(quarantine, [])
        release, lineage = lab.prepare_release(accepted, "greek-regression")
        index = {row["record_id"]: row for row in lineage}
        self.assertEqual(index["a"]["canonical_id"], index["b"]["canonical_id"])
        self.assertEqual(len({index[item]["group_id"] for item in "abc"}), 1)
        self.assertEqual(len({index[item]["split"] for item in "abc"}), 1)
        self.assertEqual(len(release), 4)
        self.assertEqual(sum(row["text"] == "\u0390" for row in release), 1)
        self.assertEqual({row["split"] for row in release}, {"train", "dev", "test"})

    def test_malformed_rows_are_quarantined_with_exact_bytes(self):
        good = lab.jsonl_bytes([self.record("ok", "A usable row")])
        invalid = [b'{"id":\n', b'[]\n', b'\xff\n', b'\n',
                   b'{"id":"same","id":"again"}\n', b'{"value":NaN}\n',
                   lab.jsonl_bytes([self.record("empty", " \t")]),
                   lab.jsonl_bytes([self.record("wrong", 12)]),
                   lab.jsonl_bytes([{**self.record("extra", "hello"), "gold": "billing"}]),
                   b'{"id":"surrogate","source_id":"s","family_id":"f","text":"\\ud800"}\n']
        accepted, quarantined = lab.read_records(good + b"".join(invalid))
        self.assertEqual([row["id"] for row in accepted], ["ok"])
        self.assertEqual(len(quarantined), len(invalid))
        for expected, actual in zip(invalid, quarantined):
            self.assertEqual(base64.b64decode(actual["raw_line_base64"]), expected)
            self.assertEqual(actual["raw_line_sha256"], hashlib.sha256(expected).hexdigest())
            self.assertTrue(actual["reason"])

    def test_missing_or_invalid_record_ids_are_quarantined(self):
        examples = [self.record("ok", "valid")]
        for field in ("id", "source_id", "family_id"):
            missing = self.record("missing-" + field, "text")
            del missing[field]
            examples.append(missing)
            examples.append({**self.record("empty-" + field, "text"), field: ""})
        examples.append(self.record("space in id", "text"))
        accepted, quarantined = lab.read_records(lab.jsonl_bytes(examples))
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(quarantined), 7)

    def test_duplicate_record_ids_quarantine_all_occurrences(self):
        examples = [self.record("collision", "first"), self.record("good", "valid"),
                    self.record("collision", "second")]
        for ordering in (examples, list(reversed(examples))):
            accepted, quarantined = lab.read_records(lab.jsonl_bytes(ordering))
            self.assertEqual([row["id"] for row in accepted], ["good"])
            self.assertEqual(len(quarantined), 2)
            self.assertTrue(all(row["reason"] == "duplicate record id: collision" for row in quarantined))

    def test_invalid_duplicate_reserves_unambiguous_id_in_both_orders(self):
        examples = [self.record("collision", "valid text"),
                    self.record("good", "another valid text"),
                    {**self.record("collision", "bad text"), "extra": True}]
        for ordering in (examples, list(reversed(examples))):
            accepted, quarantined = lab.read_records(lab.jsonl_bytes(ordering))
            self.assertEqual([row["id"] for row in accepted], ["good"])
            self.assertEqual(len(quarantined), 2)
            self.assertEqual(sum(row["reason"] == "duplicate record id: collision"
                                 for row in quarantined), 1)
            self.assertEqual(sorted(row["source_line"] for row in accepted + quarantined), [1, 2, 3])

    def test_duplicate_key_object_does_not_guess_record_identity(self):
        data = lab.jsonl_bytes([self.record("collision", "valid text")])
        data += b'{"id":"collision","id":"ambiguous","text":"bad"}\n'
        accepted, quarantined = lab.read_records(data)
        self.assertEqual([row["id"] for row in accepted], ["collision"])
        self.assertEqual(len(quarantined), 1)
        self.assertIn("duplicate JSON key", quarantined[0]["reason"])

    def test_reference_input_is_retained_for_exact_audit_reproduction(self):
        out = self.build_fixture()
        raw = (LAB / "data/gold.json").read_bytes()
        self.assertEqual((out / "reference/gold.json").read_bytes(), raw)
        manifest = json.loads((out / "manifest.json").read_text())
        self.assertEqual(manifest["outputs"]["reference/gold.json"]["sha256"], hashlib.sha256(raw).hexdigest())

    def test_full_raw_preservation_and_lineage(self):
        out = self.build_fixture()
        source_bytes = (LAB / "data" / "records.jsonl").read_bytes()
        self.assertEqual((out / "raw" / "records.jsonl").read_bytes(), source_bytes)
        original_lines = source_bytes.splitlines(keepends=True)
        lineage = rows(out / "lineage.jsonl")
        quarantine = rows(out / "quarantine.jsonl")
        self.assertEqual(sorted(row["source_line"] for row in lineage + quarantine),
                         list(range(1, 31)))
        for row in lineage + quarantine:
            raw = original_lines[row["source_line"] - 1]
            self.assertEqual(base64.b64decode(row["raw_line_base64"]), raw)
            self.assertEqual(row["raw_line_sha256"], hashlib.sha256(raw).hexdigest())
        for row in lineage:
            self.assertEqual(row["raw_text_sha256"], hashlib.sha256(row["raw_text"].encode()).hexdigest())
        index = {row["record_id"]: row for row in lineage}
        self.assertEqual(index["r01"]["canonical_id"], index["r02"]["canonical_id"])
        self.assertNotEqual(index["r01"]["raw_text"], index["r02"]["raw_text"])

    def test_union_is_transitive_across_duplicates_sources_and_families(self):
        examples = [self.record("a", "Invoice", family="shared-family"),
                    self.record("b", "Different wording", family="shared-family"),
                    self.record("c", " INVOICE ", source="shared-source"),
                    self.record("d", "Another wording", source="shared-source"),
                    self.record("e", "Independent alpha"), self.record("f", "Independent beta")]
        accepted, _ = lab.read_records(lab.jsonl_bytes(examples))
        release, lineage = lab.prepare_release(accepted, "test-seed")
        index = {row["record_id"]: row for row in lineage}
        self.assertEqual(len({index[item]["group_id"] for item in "abcd"}), 1)
        self.assertEqual(len({index[item]["split"] for item in "abcd"}), 1)
        self.assertEqual(index["a"]["canonical_id"], index["c"]["canonical_id"])
        self.assertEqual(len(release), 5)
        self.assertEqual({row["split"] for row in release}, {"train", "dev", "test"})

    def test_nonempty_splits_have_no_relation_overlap(self):
        out = self.build_fixture()
        release = rows(out / "release.jsonl")
        all_split_rows = []
        for split in ("train", "dev", "test"):
            selected = rows(out / (split + ".jsonl"))
            self.assertTrue(selected)
            self.assertTrue(all(row["split"] == split for row in selected))
            all_split_rows.extend(selected)
        self.assertEqual(sorted(all_split_rows, key=lambda row: row["canonical_id"]), release)
        lineage = rows(out / "lineage.jsonl")
        for relation in ("canonical_id", "group_id", "source_id", "family_id"):
            assignments = {}
            for row in lineage:
                assignments.setdefault(row[relation], set()).add(row["split"])
            self.assertTrue(all(len(splits) == 1 for splits in assignments.values()), relation)

    def test_too_few_leakage_groups_fails_instead_of_leaking(self):
        accepted, _ = lab.read_records(lab.jsonl_bytes([
            self.record("a", "Invoice"), self.record("b", "Crash")]))
        with self.assertRaisesRegex(ValueError, "at least 3 leakage groups"):
            lab.prepare_release(accepted, "seed")

    def test_conflicting_duplicate_gold_is_excluded_not_majority_voted(self):
        examples = [self.record("a", "Invoice"), self.record("b", " INVOICE "),
                    self.record("c", "Password"), self.record("d", "Error")]
        records_path, gold_path = self.write_inputs(examples, {"a": "billing", "b": "technical",
                                                              "c": "access", "d": "technical"})
        out = self.build_fixture(records=records_path, gold=gold_path)
        audit = json.loads((out / "audit.json").read_text())
        self.assertEqual(audit["gold"]["conflicting_canonical_examples"], 1)
        self.assertEqual(audit["weak_labels"]["evaluated_predictions"], 2)
        conflict = audit["gold"]["conflicts"][0]
        self.assertEqual({item["record_id"] for item in conflict["annotations"]}, {"a", "b"})
        self.assertEqual(audit["per_rule"]["billing_terms"]["evaluated_predictions"], 0)
        self.assertIsNone(audit["per_rule"]["billing_terms"]["accuracy"])

    def test_gold_changes_cannot_change_release_predictions_or_splits(self):
        first = self.build_fixture("first")
        gold = json.loads((LAB / "data" / "gold.json").read_text())
        gold["labels"] = {key: "technical" for key in gold["labels"]}
        changed = self.work / "changed-gold.json"
        changed.write_bytes(lab.json_bytes(gold))
        second = self.build_fixture("second", gold=changed)
        for name in ("release.jsonl", "train.jsonl", "dev.jsonl", "test.jsonl", "lineage.jsonl"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes(), name)
        self.assertNotEqual((first / "audit.json").read_bytes(), (second / "audit.json").read_bytes())
        for row in rows(first / "release.jsonl"):
            self.assertEqual(set(row), {"canonical_id", "text", "group_id", "split", "rule_votes",
                                        "weak_label", "label_status"})

    def test_unknown_or_quarantined_gold_id_fails_before_output(self):
        for unknown in ("does-not-exist", "missing-family"):
            gold = self.work / "unknown.json"
            gold.write_bytes(lab.json_bytes({"provenance": "Test labels", "labels": {unknown: "billing"}}))
            with self.assertRaisesRegex(ValueError, "unknown or quarantined"):
                self.build_fixture(gold=gold)
            self.assertFalse((self.work / "release").exists())

    def test_missing_gold_and_invalid_gold_are_not_silently_filled(self):
        empty = self.work / "empty-gold.json"
        empty.write_bytes(lab.json_bytes({"provenance": "No annotations yet", "labels": {}}))
        out = self.build_fixture(gold=empty)
        audit = json.loads((out / "audit.json").read_text())
        self.assertEqual(audit["gold"]["missing_canonical_examples"], 24)
        self.assertEqual(audit["weak_labels"]["evaluated_predictions"], 0)
        self.assertIsNone(audit["weak_labels"]["accuracy"])
        for bad in ({"labels": {}}, {"labels": {"r01": "other"}, "provenance": "Test"},
                    {"labels": {"r01": ["billing"]}, "provenance": "Test"}):
            with self.assertRaises(ValueError):
                lab.read_gold(lab.json_bytes(bad), {"r01"})
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            lab.read_gold(b'{"provenance":"Test","labels":{"r01":"billing","r01":"access"}}', {"r01"})

    def test_reordered_input_preserves_semantic_outputs(self):
        first = self.build_fixture("first")
        shuffled = self.work / "reversed.jsonl"
        shuffled.write_bytes(b"".join(reversed((LAB / "data" / "records.jsonl").read_bytes().splitlines(keepends=True))))
        second = self.build_fixture("second", records=shuffled)
        for name in ("release.jsonl", "train.jsonl", "dev.jsonl", "test.jsonl", "audit.json"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes(), name)
        # Physical provenance must change when the source file changes order.
        self.assertNotEqual((first / "raw" / "records.jsonl").read_bytes(),
                            (second / "raw" / "records.jsonl").read_bytes())
        self.assertNotEqual((first / "lineage.jsonl").read_bytes(), (second / "lineage.jsonl").read_bytes())

    def test_identical_recipe_is_byte_reproducible_at_different_paths(self):
        first, second = self.build_fixture("one"), self.build_fixture("different/path/two")
        relative_files = [path.relative_to(first) for path in first.rglob("*") if path.is_file()]
        for relative in relative_files:
            self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes(), str(relative))
        self.assertNotIn(str(self.work), (first / "manifest.json").read_text())

    def test_seed_changes_assignments_without_changing_examples_or_votes(self):
        first, second = self.build_fixture("one"), self.build_fixture("two", seed="alternate-seed")
        before, after = rows(first / "release.jsonl"), rows(second / "release.jsonl")
        self.assertNotEqual([row["split"] for row in before], [row["split"] for row in after])
        self.assertEqual([{key: value for key, value in row.items() if key != "split"} for row in before],
                         [{key: value for key, value in row.items() if key != "split"} for row in after])
        manifest = json.loads((second / "manifest.json").read_text())
        self.assertEqual(manifest["recipe"]["seed"], "alternate-seed")

    def test_manifest_hashes_every_output_and_recipe(self):
        out = self.build_fixture()
        manifest = json.loads((out / "manifest.json").read_text())
        names = {path.relative_to(out).as_posix() for path in out.rglob("*") if path.is_file()}
        self.assertEqual(set(manifest["outputs"]), names - {"manifest.json"})
        for name, metadata in manifest["outputs"].items():
            content = (out / name).read_bytes()
            self.assertEqual(metadata, {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
        self.assertEqual(manifest["recipe_sha256"], hashlib.sha256(lab.json_bytes(manifest["recipe"])).hexdigest())
        for name, source in (("records.jsonl", LAB / "data" / "records.jsonl"),
                             ("gold.json", LAB / "data" / "gold.json"), ("build.py", LAB / "build.py")):
            self.assertEqual(manifest["inputs"][name]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(manifest["recipe"]["seed"], lab.DEFAULT_SEED)
        self.assertEqual(manifest["recipe"]["version"], 3)
        self.assertIn("NFKC, casefold, NFKC again", manifest["recipe"]["normalization"])

    def test_rule_coverage_and_accuracy_counts_are_measured(self):
        out = self.build_fixture()
        audit = json.loads((out / "audit.json").read_text())
        release = rows(out / "release.jsonl")
        for name, metrics in audit["per_rule"].items():
            votes = sum(row["rule_votes"][name] is not None for row in release)
            self.assertEqual(metrics["coverage"]["voted_examples"], votes)
            self.assertEqual(metrics["coverage"]["eligible_examples"], len(release))
            self.assertEqual(metrics["coverage"]["coverage"], votes / len(release))
            self.assertLessEqual(metrics["correct"], metrics["evaluated_predictions"])
            self.assertLessEqual(metrics["evaluated_predictions"], votes)

    def test_nonempty_output_refused_without_changes_and_empty_allowed(self):
        out = self.work / "occupied"
        out.mkdir()
        (out / "keep.txt").write_text("do not overwrite")
        with self.assertRaisesRegex(ValueError, "nonexistent or empty"):
            self.build_fixture("occupied")
        self.assertEqual(list(out.iterdir()), [out / "keep.txt"])
        self.assertEqual((out / "keep.txt").read_text(), "do not overwrite")
        empty = self.work / "empty"
        empty.mkdir()
        self.build_fixture("empty")
        self.assertTrue((empty / "manifest.json").is_file())
        with self.assertRaisesRegex(ValueError, "nonexistent or empty"):
            self.build_fixture("empty")

    def test_cli_success_and_repeat_failure(self):
        command = [sys.executable, "-B", str(LAB / "build.py"), "--out", str(self.work / "cli")]
        first = subprocess.run(command, cwd=self.work, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["counts"]["canonical_examples"], 24)
        second = subprocess.run(command, cwd=self.work, capture_output=True, text=True)
        self.assertEqual(second.returncode, 2)
        self.assertIn("output must be", second.stderr)


if __name__ == "__main__":
    unittest.main()
