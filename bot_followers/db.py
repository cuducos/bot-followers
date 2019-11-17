from math import sqrt
from pathlib import Path

import click
from peewee import CharField, FloatField, Model, SqliteDatabase


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

    def error(self, number):
        z_score = 1.96  # 0.95 confidence
        proportion = self.percent(number)
        return z_score * sqrt(proportion * (1 - proportion) / self.count)

    def percent(self, number):
        match = self.users.where(User.botometer >= number).count()
        return match / self.count
