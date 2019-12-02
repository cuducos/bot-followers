from celery import shared_task
from celery.task.control import revoke

from web.core.external.botometer import botometer
from web.core.external.twitter import Twitter
from web.core.models import Account, Job


@shared_task
def start(pk):
    job = Job.objects.get(pk=pk)
    twitter = Twitter(job.screen_name)

    job.total_followers = twitter.total_followers
    job.save()

    for user in twitter.followers:
        check_account.delay(user.screen_name, job.pk)


@shared_task
def check_account(screen_name, pk):
    job = Job.objects.get(pk=pk)
    account, _ = Account.objects.get_or_create(
        screen_name=screen_name, defaults={"screen_name": screen_name}
    )

    account.follower_of.add(job)
    if account.needs_update():
        check_botometer.delay(account.pk, job.pk)


@shared_task
def check_botometer(account_pk, job_pk):
    account = Account.objects.get(pk=account_pk)
    account.botometer = botometer(account.screen_name)
    account.save()


@shared_task
def pause(pk):
    job = Job.objects.get(pk=pk)
    revoke(job.celery_task_id, terminate=True)
