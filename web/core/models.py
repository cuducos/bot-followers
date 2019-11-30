from math import sqrt

from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    def accounts(self):
        return self.account_set.exclude(botometer=None)

    def total(self):
        return self.accounts().count()

    def percent_over(self, number):
        match = self.accounts().filter(botometer__gte=number).count()
        percent = match / self.total()
        z_score = 1.96  # 0.95 confidence
        error = z_score * sqrt(percent * (1 - percent) / self.total())
        return percent, error

    class Meta:
        ordering = ("screen_name",)
        verbose_name = "report"


class Account(models.Model):
    screen_name = LowerCaseCharField(max_length=15, unique=True, db_index=True)
    botometer = models.FloatField(db_index=True, null=True)
    follower_of = models.ManyToManyField(Job, db_index=True)
    last_update = models.DateTimeField(auto_now=True)
