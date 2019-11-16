from math import sqrt
from pathlib import Path
from statistics import stdev

import click
from peewee import CharField, FloatField, Model, SqliteDatabase


def humanized_percent(number, decimals=0):
    result = round(number * 100, decimals) if decimals else round(number * 100)
    return f"{result}%"


class User(Model):
    screen_name = CharField(max_length=15, unique=True, primary_key=True, index=True)
    botometer = FloatField(index=True, null=True)


class Database:
    def __init__(self, target):
        self.target = target
        self.path = Path(f"{target.screen_name.lower()}.sqlite3").resolve()
        self._count = None

    def __enter__(self):
        click.echo(f"Spinning up the database at {self.path}…")
        self.path.touch()
        db = SqliteDatabase(str(self.path))
        User.bind(db)
        User.create_table(safe=True)
        return self

    def __exit__(self, *args):
        click.echo("Cleaning-up…")
        if self.count:
            User.delete().where(User.botometer is None).execute()
        else:
            self.path.unlink()

    def save(self, user, check_if_already_exists=False):
        if check_if_already_exists:
            if User.select().where(User.screen_name == user.screen_name).exists():
                return

        record = User.create(screen_name=user.screen_name)
        user.query_botometer()
        record.botometer = user.botometer
        record.save()

    @property
    def users(self):
        return User.select().where(User.botometer is not None)

    @property
    def count(self):
        if self._count is not None:
            return self._count
        self._count = self.users.count()
        return self._count

    @property
    def error(self):
        z_score = 1.96  # 0.95 confidence
        sample = (u.botometer for u in self.users if isinstance(u.botometer, float))
        return z_score * (stdev(sample) / sqrt(self.count))

    def percent(self, number):
        match = self.users.where(User.botometer >= number).count()
        return match / self.count

    def report(self):
        data = {
            "Total followers": f"{self.target.followers_count:,}",
            "Followers analyzed": f"{self.count:,}",
            "Percentage analyzed": humanized_percent(
                self.count / self.target.followers_count, 2
            ),
            "Margin of error (95% confidence)": f"{self.error:.4f}\n",
        }

        for number in (0.5, 0.75, 0.8, 0.9, 0.95):
            label = f"Accounts with +{humanized_percent(number)} in Botometer"
            data[label] = humanized_percent(self.percent(number), 2)

        click.echo(f"\nAnalysis of @{self.target.screen_name}'s followers\n")
        largest = max(len(key) for key in data.keys())
        for key, value in data.items():
            label = key.ljust(largest + 2, ".")
            click.echo(f"{label}: {value}")
        click.echo(" ")
