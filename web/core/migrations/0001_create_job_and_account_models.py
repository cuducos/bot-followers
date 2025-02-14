# Generated by Django 2.2.7 on 2019-11-30 17:42

from django.db import migrations, models

import web.core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "screen_name",
                    web.core.models.LowerCaseCharField(
                        db_index=True, max_length=15, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "screen_name",
                    web.core.models.LowerCaseCharField(
                        db_index=True, max_length=15, unique=True
                    ),
                ),
                ("botometer", models.FloatField(db_index=True, null=True)),
                ("last_update", models.DateTimeField(auto_now=True)),
                ("follower_of", models.ManyToManyField(db_index=True, to="core.Job")),
            ],
        ),
    ]
