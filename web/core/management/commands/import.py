from dataclasses import dataclass
from pathlib import Path
from sqlite3 import connect

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from tqdm import tqdm
from tweepy import API

from web.core.external.authentication import authentication
from web.core.models import Account, Job


@dataclass
class LegacyDatabase:
    path: Path

    def __enter__(self):
        self.connection = connect(str(self.path))
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *args, **kwargs):
        self.connection.close()

    def count(self):
        self.cursor.execute("SELECT COUNT(screen_name) FROM user")
        total, *_ = self.cursor.fetchone()
        return total

    def rows(self):
        self.cursor.execute("SELECT screen_name, botometer FROM user")
        for screen_name, botometer in self.cursor.fetchall():
            yield {"screen_name": screen_name, "botometer": botometer}


class Command(BaseCommand):
    help = "Import databases from Bot Followers CLI version"

    def add_arguments(self, parser):
        parser.add_argument("sqlite", nargs="+", help="Path to a SQLite3 file")

    def handle(self, *args, **options):
        self.paths = tuple(Path(path).absolute() for path in options["sqlite"])
        for path in self.paths:
            if not path.exists():
                raise CommandError(f"{path} does not exist.")
            if not path.is_file():
                raise CommandError(f"{path} is not a file.")

        # make sure we have the job instances
        for path in self.paths:
            api = API(authentication.tweepy, wait_on_rate_limit=True)
            user = api.get_user(path.stem)
            job, _ = Job.objects.update_or_create(
                screen_name=path.stem,
                defaults={
                    "screen_name": path.stem,
                    "total_followers": user.followers_count,
                },
            )

        # prepare to import
        limit = timezone.now() - settings.CACHE_BOTOMETER_RESULTS_FOR_DAYS
        total = 0
        for path in self.paths:
            with LegacyDatabase(path) as db:
                total += db.count()

        # import followers & botometer results
        progress = tqdm(unit="record", total=total)
        for path in self.paths:
            with LegacyDatabase(path) as db:
                for row in db.rows():
                    account, is_new_account = Account.objects.get_or_create(
                        screen_name=row["screen_name"], defaults=row
                    )

                    if not is_new_account and account.last_update < limit:
                        account.botometer = row["botometer"]
                        account.save()

                    job = Job.objects.get(screen_name=path.stem)
                    if not account.follower_of.filter(pk=job.pk).exists():
                        account.follower_of.add(job)

                    progress.update(1)
