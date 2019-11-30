from django.shortcuts import resolve_url
from django.test import TestCase


class TestHomeView(TestCase):
    def test_redirects_to_admin_home(self):
        self.assertRedirects(
            self.client.get(resolve_url("home")),
            resolve_url("admin:index"),
            target_status_code=302,  # admin home will redirect to login
        )
