from django.test import TestCase

from web.core.forms import ScreenNameForm


class TestScreenNameForm(TestCase):
    def _test_screen_name(self, screen_name, valid):
        form = ScreenNameForm({"screen_name": screen_name})
        method = self.assertTrue if valid else self.assertFalse
        expected = "valid" if valid else "invalid"
        method(form.is_valid(), f"{screen_name} was supposed to be {expected}")

    def test_invalid_screen_names(self):
        screen_names = (
            None,
            "",
            "1234567890123456",
            "abcdefghijklmkno",
            "i have spaces",
            "Forbiden-Chars!",
        )
        for screen_name in screen_names:
            with self.subTest():
                self._test_screen_name(screen_name, False)

    def test_valid_screen_names(self):
        screen_names = (
            "a",
            "cuducos",
            "Borsalino",
            "234567890123456",
            "bcdefghijklmkno",
            "lettesAnd123",
        )
        for screen_name in screen_names:
            with self.subTest():
                self._test_screen_name(screen_name, True)
