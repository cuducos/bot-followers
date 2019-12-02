from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import resolve_url
from django.test import TestCase
from mixer.backend.django import mixer

from web.core.models import Job


USER = "borsalino"
PASS = "queiroz"
FORM = {"screen_name": "borsalino"}


def with_user(func):
    def inner(*args, **kwargs):
        User = get_user_model()
        user = User.objects.create_user(USER, password=PASS, is_staff=True)
        permission = Permission.objects.get(codename="view_job")
        user.user_permissions.add(permission)
        func(*args, **kwargs)

    return inner


class BaseTestJobView:
    def test_non_authenticated_user_is_not_allowed(self):
        response = self.client.post(self.URL, FORM)
        self.assertEquals(response.status_code, 403)

    @with_user
    def test_get_is_not_allowed(self):
        self.client.login(username=USER, password=PASS)
        response = self.client.get(self.URL)
        self.assertEquals(response.status_code, 405)

    @with_user
    def test_invalid_form_returns_error(self):
        self.client.login(username=USER, password=PASS)
        response = self.client.post(self.URL, {"screen_name": "face book"})
        self.assertEquals(response.status_code, 400)


class TestJobStartView(TestCase, BaseTestJobView):
    URL = resolve_url("start")

    @with_user
    @patch("web.core.views.tasks")
    def test_successful_request_with_existing_job(self, tasks):
        mixer.blend(Job, screen_name=FORM["screen_name"])
        tasks.start.delay.return_value.id = "42"

        self.client.login(username=USER, password=PASS)
        response = self.client.post(self.URL, FORM)

        job = Job.objects.get(screen_name=FORM["screen_name"])
        tasks.start.delay.assert_called_once_with(job.pk)
        self.assertEqual(job.celery_task_id, "42")
        self.assertRedirects(response, resolve_url(settings.ROOT_REDIRECTS_TO))

    @with_user
    @patch("web.core.views.tasks")
    def test_successful_request_with_non_existing_job(self, tasks):
        tasks.start.delay.return_value.id = "42"

        self.client.login(username=USER, password=PASS)
        response = self.client.post(self.URL, FORM)

        job = Job.objects.get(screen_name=FORM["screen_name"])
        tasks.start.delay.assert_called_once_with(job.pk)
        self.assertEqual(job.celery_task_id, "42")
        self.assertRedirects(response, resolve_url(settings.ROOT_REDIRECTS_TO))


class TestJobPauseView(TestCase, BaseTestJobView):
    URL = resolve_url("pause")

    @with_user
    @patch("web.core.views.tasks")
    def test_successful_request_in_existing_job(self, tasks):
        mixer.blend(Job, screen_name=FORM["screen_name"], celery_task_id="42")

        self.client.login(username=USER, password=PASS)
        response = self.client.post(self.URL, FORM)

        job = Job.objects.get(screen_name=FORM["screen_name"])
        tasks.pause.delay.assert_called_once_with(job.pk)
        self.assertEqual(job.celery_task_id, None)
        self.assertRedirects(response, resolve_url(settings.ROOT_REDIRECTS_TO))

    @with_user
    @patch("web.core.views.tasks")
    def test_successful_request_with_non_existing_job(self, tasks):
        self.client.login(username=USER, password=PASS)
        response = self.client.post(self.URL, FORM)

        tasks.pause.delay.assert_not_called()
        self.assertRedirects(response, resolve_url(settings.ROOT_REDIRECTS_TO))
