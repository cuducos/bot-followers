from django.test import TestCase

from web.core.models import Account


class TestAccountModel(TestCase):
    def setUp(self):
        self.account = Account.objects.create(screen_name="Borsalino")

    def test_save(self):
        self.assertEqual("borsalino", self.account.screen_name)

    def test_query(self):
        self.assertTrue(Account.objects.filter(screen_name="borsalino").exists())
