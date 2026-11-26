"""README validation accepts simple layouts but still catches broken content."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'validate-readme.py'
spec = importlib.util.spec_from_file_location('validate_readme', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class FlexibleLayoutTests(unittest.TestCase):
    def test_plain_readme_has_no_layout_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / 'README.md'
            readme.write_text('# Example\n\nA small tool.\n\n## Usage\n\nRun it.\n')
            errors, warnings = validator.check(readme)
            self.assertEqual(errors, [])
            self.assertTrue(any('centred top block' in warning for warning in warnings))

    def test_missing_image_and_broken_anchor_remain_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / 'README.md'
            readme.write_text('# Example\n\n[Missing](#absent)\n\n<img src="missing.png">\n')
            errors, _ = validator.check(readme)
            self.assertTrue(any('without alt' in error for error in errors))
            self.assertTrue(any('broken anchor' in error for error in errors))
            self.assertTrue(any('missing file' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
