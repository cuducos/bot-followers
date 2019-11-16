from tweepy import models

from bot_followers.botometer import BotometerResult


class User(models.User):
    """A wrapper for Tweepy native User model, including a filed with Botometer
    result to ponder whether the user might be a bot or nor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._botometer_result = None  # cache

    @classmethod
    def parse(cls, api, data):
        """This is how Tweepy instantiate User models from the API result"""
        return super(User, cls).parse(api, data)

    def query_botometer(self):
        if self.protected:
            self._botometer_result = 0.0
            return

        botometer = BotometerResult(self.id)
        self._botometer_result = botometer.probability

    @property
    def botometer(self):
        if self._botometer_result is not None:
            return self._botometer_result

        self.query_botometer()
        return self._botometer_result
