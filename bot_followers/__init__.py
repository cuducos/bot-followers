from functools import partial

import click
from tweepy import API, Cursor

from bot_followers.authentication import authentication
from bot_followers.user import User
from bot_followers.db import Database


def humanized_percent(number, decimals=2):
    result = round(number * 100, decimals) if decimals else round(number * 100)
    return f"{result}%"


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
            with click.progressbar(self.followers, **kwargs) as users:
                for user in users:
                    db.save(user, check_if_already_exists=True)

    def report(self):
        with Database(self.target) as db:
            data = {
                "Total followers": f"{self.target.followers_count:,}",
                "Followers analyzed": f"{db.count:,}",
                "Percentage analyzed": humanized_percent(
                    db.count / self.target.followers_count
                ),
                "": "",
            }

            for number in (50, 75, 80, 90, 95):
                label = f"Accounts with +{number}% in Botometer"
                result = humanized_percent(db.percent(number / 100))
                error = humanized_percent(db.error(number / 100))
                data[label] = f"{result} (±{error})"

            click.echo()
            click.echo(f"Analysis of @{self.target.screen_name}'s followers")
            click.echo()

            largest = max(len(key) for key in data.keys())
            for key, value in data.items():
                if not value:
                    click.echo()
                    continue

                label = key.ljust(largest + 2, ".")
                click.echo(f"{label}: {value}")

            click.echo("")
