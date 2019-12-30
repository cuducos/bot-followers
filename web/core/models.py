from math import sqrt

from django.conf import settings
from django.db import models
from django.utils import timezone

from web.core.fields import LowerCaseCharField
from web.core.querysets import AccountQuerySet, JobQuerySet
from web.core.serializers import JobSerializer


class Job(models.Model, JobSerializer):
    screen_name = LowerCaseCharField(max_length=15, unique=True, db_index=True)
    image = models.URLField(default="", blank=True)
    total_followers = models.IntegerField(null=True)
    celery_task_id = models.CharField(
        max_length=155, unique=True, db_index=True, default=None, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = JobQuerySet.as_manager()

    def percent_over(self, number, over_or_equal=True, wrapper=None):
        if not self.followers.analyzed().exists():
            return ''

        equal = "e" if over_or_equal else ""
        kwargs = {f"botometer__gt{equal}": number}
        macth_count = self.followers.analyzed().filter(**kwargs).count()

        total = self.followers.analyzed().count()
        percent = macth_count / total
        error = settings.Z_SCORE * sqrt(percent * (1 - percent) / total)
        return wrapper(percent, error) if wrapper else (percent, error)

    def save_task(self, task_id):
        self.celery_task_id = task_id
        self.save()

    class Meta:
        ordering = ("screen_name",)
        verbose_name = "report"


class Account(models.Model):
    screen_name = LowerCaseCharField(max_length=15, unique=True, db_index=True)
    botometer = models.FloatField(db_index=True, null=True)
    follower_of = models.ManyToManyField(Job, related_name="followers", db_index=True)
    last_update = models.DateTimeField(auto_now=True)

    objects = AccountQuerySet.as_manager()

    def needs_update(self):
        if self.botometer is None:
            return True

        limit = timezone.now() - settings.CACHE_BOTOMETER_RESULTS_FOR_DAYS
        return self.last_update < limit
