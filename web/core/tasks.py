from celery import shared_task
from celery.task.control import revoke
from tweepy import RateLimitError

from lib.botometer import botometer
from lib.twitter import Twitter
from web.core.models import Account, Job


def status(job, message):
    screen_name = job.screen_name if isinstance(job, Job) else job
    return f"@{screen_name}'s job: {message}"


def restart(job):
    task = start.delay(job.pk)
    job.save_task(task.id)
    return status(job, "re-started")


@shared_task
def start(pk):
    job = Job.objects.get(pk=pk)
    try:
        twitter = Twitter(job.screen_name)
    except RateLimitError:
        return restart(job)

    job.total_followers = twitter.total_followers
    job.image = twitter.image
    job.save()

    try:
        for user in twitter.followers:
            check_account.delay(user.screen_name, job.pk)
    except RateLimitError:
        return restart(job)


@shared_task
def check_account(screen_name, pk):
    job = Job.objects.get(pk=pk)
    user, _ = Account.objects.get_or_create(
        screen_name=screen_name, defaults={"screen_name": screen_name}
    )

    user.follower_of.add(job)
    if not user.needs_update():
        return status(job, f"@{user.screen_name} skipped (using cache).")

    check_botometer.delay(user.pk, job.pk)
    return status(job, f"@{user.screen_name}'s Botometer test scheduled.")


@shared_task
def check_botometer(user_pk, job_pk):
    job = Job.objects.get(pk=job_pk)
    user = Account.objects.get(pk=user_pk)

    try:
        user.botometer = botometer(user.screen_name)
    except RateLimitError:
        check_botometer.delay(user_pk, job_pk)
        msg = "re-scheduled"
    else:
        msg = "fetched"
        user.save()

    return status(job, f"@{user.screen_name}'s Botometer score {msg}.")


@shared_task
def pause(pk):
    job = Job.objects.get(pk=pk)
    revoke(job.celery_task_id, terminate=True)
    return status(job, "stopped")
