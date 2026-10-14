"""Selector source contracts; actual browser execution remains required."""
import ast
import html
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BrowserHarnessTests(unittest.TestCase):
    def test_exact_button_names_match_one_literal_app_template(self):
        app = (ROOT / 'docs/app.js').read_text()
        labels = [html.unescape(re.sub(r'<[^>]+>', '', label)).strip()
                  for label in re.findall(r'<button\b[^>]*>(.*?)</button>', app, re.S)
                  if '${' not in label]
        tree = ast.parse((ROOT / 'tests/browser_qa.py').read_text())
        count = 0
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != 'get_by_role' or not node.args or not isinstance(node.args[0], ast.Constant):
                continue
            if node.args[0].value != 'button':
                continue
            keywords = {item.arg: item.value for item in node.keywords}
            name = keywords.get('name')
            if not isinstance(name, ast.Constant):
                continue
            self.assertIs(keywords['exact'].value, True)
            self.assertEqual(labels.count(name.value), 1, name.value)
            count += 1
        self.assertGreater(count, 20)

    def test_badge_semantics_do_not_depend_on_css_text_casing(self):
        source = (ROOT / 'tests/browser_qa.py').read_text()
        self.assertNotIn("page.inner_text('main')", source)
        self.assertIn("page.locator('.hero .meta-row')", source)
        self.assertIn("get_by_text('1 leaking family', exact=True)", source)
        self.assertIn("filter(has_text='needs-review')", source)
        self.assertIn("get_by_text('Proposed interface', exact=True)", source)


if __name__ == '__main__':
    unittest.main()
