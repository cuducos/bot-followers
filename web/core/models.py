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
    created_at = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    screen_name = LowerCaseCharField(max_length=15, unique=True, db_index=True)
    botometer = models.FloatField(db_index=True, null=True)
    follower_of = models.ManyToManyField(Job, db_index=True)
    last_update = models.DateTimeField(auto_now=True)
