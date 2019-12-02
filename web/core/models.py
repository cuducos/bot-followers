from math import sqrt

from django.conf import settings
from django.db import models
from django.utils import timezone


class LowerCaseCharField(models.CharField):
    def pre_save(self, instance, add):
        value = getattr(instance, self.attname)
        setattr(instance, self.attname, value.lower())
        return super(LowerCaseCharField, self).pre_save(instance, add)

    def to_python(self, value):
        value = super(LowerCaseCharField, self).to_python(value)
        return value.lower()


class Job(models.Model):
    screen_name = LowerCaseCharField(max_length=15, unique=True, db_index=True)
    total_followers = models.IntegerField(null=True)
    celery_task_id = models.CharField(
        max_length=155, unique=True, db_index=True, default=None, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def accounts(self):
        return self.account_set.exclude(botometer=None)

    def total(self):
        return self.accounts().count()

    def percent_over(self, number):
        if not self.total():
            return None, None

        match = self.accounts().filter(botometer__gte=number).count()
        percent = match / self.total()
        z_score = 1.96  # 0.95 confidence
        error = z_score * sqrt(percent * (1 - percent) / self.total())
        return percent, error

    def save_task(self, task_id):
        self.celery_task_id = task_id
        self.save()

    class Meta:
        ordering = ("screen_name",)
        verbose_name = "report"


class Account(models.Model):
    screen_name = LowerCaseCharField(max_length=15, unique=True, db_index=True)
    botometer = models.FloatField(db_index=True, null=True)
    follower_of = models.ManyToManyField(Job, db_index=True)
    last_update = models.DateTimeField(auto_now=True)

    def needs_update(self):
        if self.botometer is None:
            return True

        limit = timezone.now() - settings.CACHE_BOTOMETER_RESULTS_FOR_DAYS
        return self.last_update < limit
