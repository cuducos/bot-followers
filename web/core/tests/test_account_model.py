from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from mixer.backend.django import mixer

from web.core.models import Account


class TestAccountModel(TestCase):
    def setUp(self):
        self.account = mixer.blend(Account, screen_name="Borsalino")

    def test_save(self):
        self.assertEqual("borsalino", self.account.screen_name)

    def test_query(self):
        self.assertTrue(Account.objects.filter(screen_name="borsalino").exists())

    def test_needs_update_with_empty_account(self):
        self.account.botometer = None
        self.account.save()
        self.assertTrue(self.account.needs_update())

    def test_needs_update_with_new_account(self):
        self.account.botometer = 0.5
        self.account.save()
        self.assertFalse(self.account.needs_update())

    def test_needs_update_with_old_account(self):
        last_year = timezone.now() - timedelta(days=365)
        with freeze_time(last_year):
            self.account.botometer = 0.5
            self.account.save()
        self.assertTrue(self.account.needs_update())
