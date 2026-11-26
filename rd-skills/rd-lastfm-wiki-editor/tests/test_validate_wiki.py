"""Run from this skill directory: python3 -m unittest discover -s tests -v"""
import importlib.util
from pathlib import Path
import unittest

script = Path(__file__).resolve().parents[1] / "scripts" / "validate_wiki.py"
spec = importlib.util.spec_from_file_location("validate_wiki", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class WikiValidatorTests(unittest.TestCase):
    def assert_passes(self, text):
        errors, warnings = module.validate(text)
        self.assertEqual(errors, [], errors)
        self.assertEqual(warnings, [], warnings)

    def assert_fails(self, text):
        errors, _warnings = module.validate(text)
        self.assertTrue(errors, "Expected at least one lint error")

    def test_native_bbcode(self):
        self.assert_passes(
            "[b]Release History[/b]\nA recording on "
            "[album artist=Example Artist]Example Album[/album] features "
            "[track artist=Example Artist]Example Track[/track] in "
            "[tag]death metal[/tag]."
        )

    def test_valid_internal_url(self):
        self.assert_passes("See [url=https://www.last.fm/]Last.fm[/url].")
        self.assert_passes("See [url]https://www.last.fm/[/url].")

    def test_reject_external_url(self):
        self.assert_fails("See [url=https://example.org/]a link[/url].")
        self.assert_fails("More at https://music.example.org/about.")
        self.assert_fails("See [url]https://example.org/[/url].")
        self.assert_fails("See www.example.com for details.")

    def test_reject_missing_artist_attribute(self):
        self.assert_fails("It included [album]Album Name[/album].")
        self.assert_fails("They recorded [track artist=]A Song[/track].")

    def test_reject_unbalanced_tags(self):
        self.assert_fails("[b]A heading")
        self.assert_fails("[b]A heading[/i]")
        self.assert_fails("Text[/artist]")

    def test_reject_markdown(self):
        self.assert_fails("## Career\nMusic history.")
        self.assert_fails("**Career**\nMusic history.")
        self.assert_fails("* Artist details")
        self.assert_fails("Read [this](https://www.last.fm/help/markup).")

    def test_list_warning(self):
        errors, warnings = module.validate("[ulist][li]Example[/li][/ulist]")
        self.assertEqual(errors, [])
        self.assertTrue(warnings)

    def test_event_id(self):
        self.assert_passes("The [event=207155]event[/event] took place.")
        self.assert_fails("The [event=abc]event[/event] took place.")

    def test_empty(self):
        self.assert_fails("  \n")


if __name__ == "__main__":
    unittest.main()
