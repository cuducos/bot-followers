from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase


class TestHomeView(TestCase):
    def test_redirects_to_job_admin_page(self):
        self.assertRedirects(
            self.client.get(resolve_url("home")),
            resolve_url(settings.MAIN_ADMIN_VIEW),
            target_status_code=302,  # admin home will redirect to login
        )
