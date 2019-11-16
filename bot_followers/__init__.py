from functools import partial

from click import progressbar
from tweepy import API, Cursor

from bot_followers.authentication import authentication
from bot_followers.user import User
from bot_followers.db import Database


class BotFollowers:
    """Core class of this package, holding the methods to clean up the
    authenticated Twitter account."""

    def __init__(self, target):
        self.api = API(authentication.tweepy, wait_on_rate_limit=True)
        self.target = self.api.get_user(target)
        self.serialize = partial(User.parse, self.api)

    @property
    def followers(self):
        kwargs = {"screen_name": self.target.screen_name}
        for user in Cursor(self.api.followers, **kwargs).items():
            yield self.serialize(user._json)

    def __call__(self):
        kwargs = {"length": self.target.followers_count}
        with Database(self.target) as db:
            with progressbar(self.followers, **kwargs) as users:
                for user in users:
                    db.save(user, check_if_already_exists=True)

    def report(self):
        with Database(self.target) as db:
            db.report()
