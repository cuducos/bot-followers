from os import getcwd

from django.conf import settings
from tweepy import OAuthHandler


class Authentication:
    """Holds authentication data for further usage in the script"""

    def __init__(self):
        self.consumer_key = settings.TWITTER_CONSUMER_KEY
        self.consumer_secret = settings.TWITTER_CONSUMER_SECRET
        self.access_token = settings.TWITTER_ACCESS_TOKEN_KEY
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        self.mashape_key = settings.BOTOMETER_MASHAPE_KEY

    @property
    def tweepy(self):
        """Returns an authentication object required by Tweepy"""
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth

    @property
    def botometer(self):
        """Returns a dictionary compatible with Botometer API"""
        return dict(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            mashape_key=self.mashape_key,
        )


authentication = Authentication()
