from re import match

from django import forms
from django.core.exceptions import ValidationError


TWITTER_SCREEN_NAME = r"^[a-zA-Z0-9_]{1,15}$"


class ScreenNameForm(forms.Form):
    screen_name = forms.CharField(required=True, max_length=15, min_length=1)

    def clean_screen_name(self):
        screen_name = self.cleaned_data.get("screen_name")

        if not match(TWITTER_SCREEN_NAME, screen_name):
            msg = f"{screen_name} is an invalid Twitter screen name."
            raise ValidationError(msg, "screen_name")

        return screen_name
