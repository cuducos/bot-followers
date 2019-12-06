from celery.task.control import inspect
from django.core.management.base import BaseCommand
from tqdm import tqdm

from web.core.models import Job


class Command(BaseCommand):
    help = "Remove non-existing Celery tasks from the database"

    def handle(self, *args, **options):
        nodes = inspect().active()
        if not nodes:
            self.stdout.write("Done!")
            return

        tasks = set(task["id"] for node in nodes.values() for task in node)
        jobs = Job.objects.exclude(celery_task_id=None)

        if not jobs.exists():
            self.stdout.write("Done!")
            return

        for job in tqdm(jobs, unit="job"):
            if job.celery_task_id in tasks:
                continue

            job.celery_task_id = None
            job.save()
