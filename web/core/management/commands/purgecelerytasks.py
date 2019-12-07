from django.core.management import call_command
from django.core.management.base import BaseCommand

from web.core.celery import app


class Command(BaseCommand):
    help = "Remove non-started Celery tasks"

    def handle(self, *args, **options):
        app.control.purge()
        call_command("updatecelerytasks")
