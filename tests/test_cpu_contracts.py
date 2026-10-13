"""Include the standalone consumer/recovery exercises in the aggregate suite."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_tests(loader, suite, pattern):
    for identity, path in [
        ('educational_consumer_tests', ROOT / 'examples/consumer-contract/tests/test_consumer_contract.py'),
        ('educational_recovery_tests', ROOT / 'examples/recovery/tests/test_recovery.py'),
    ]:
        spec = importlib.util.spec_from_file_location(identity, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite
