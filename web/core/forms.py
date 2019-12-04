from string import ascii_letters, digits

from django import forms
from django.core.exceptions import ValidationError


class TwitterScreenNameField(forms.CharField):
    """Implements Twitter username rules as in:
    https://help.twitter.com/en/managing-your-account/twitter-username-rules
    In sum: from 1 to 15 characrters, including ASCII letters, numbers and
    underscore."""

    def __init__(self, **kwargs):
        kwargs["max_length"] = 15
        kwargs["min_length"] = 1
        super().__init__(**kwargs)
        self.validators.append(self.validate_twitter_screen_name)

    @staticmethod
    def validate_twitter_screen_name(screen_name):
        allowed_chars = set(ascii_letters + digits + "_")
        if not set(screen_name).issubset(allowed_chars):
            msg = f"{screen_name} is an invalid Twitter screen name."
            raise ValidationError(msg)


class ScreenNameForm(forms.Form):
    screen_name = TwitterScreenNameField(required=True)
