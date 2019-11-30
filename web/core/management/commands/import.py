from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from sqlite3 import connect

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from tqdm import tqdm

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
        parser.add_argument("sqlite", help="Path to a SQLite3 file")

    def handle(self, *args, **options):
        self.path = Path(options["sqlite"]).absolute()
        if not self.path.exists():
            raise CommandError(f"{self.path} does not exist.")
        if not self.path.is_file():
            raise CommandError(f"{self.path} is not a file.")

        # make sure we have a job instance
        job_data = {"screen_name": self.path.stem}
        job, _ = Job.objects.get_or_create(**job_data, defaults=job_data)

        six_months_ago = timezone.now() - timedelta(days=180)
        with LegacyDatabase(self.path) as db:
            total = db.count()
            progress = tqdm(unit="record", total=total)

            for row in db.rows():
                account, is_new_account = Account.objects.get_or_create(
                    screen_name=row["screen_name"], defaults=row
                )

                if not is_new_account and account.last_update < six_months_ago:
                    account.botometer = row["botometer"]
                    account.save()

                if not account.follower_of.filter(pk=job.pk).exists():
                    account.follower_of.add(job)

                progress.update(1)
