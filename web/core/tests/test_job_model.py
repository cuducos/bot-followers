from django.test import TestCase
from mixer.backend.django import mixer

from web.core.models import Account, Job


class TestJobModel(TestCase):
    def setUp(self):
        self.job = mixer.blend(Job, screen_name="Borsalino")
        accounts = (
            mixer.blend(Account, botometer=0.62),
            mixer.blend(Account, botometer=0.99),
            mixer.blend(Account, botometer=None),
        )
        for account in accounts:
            account.follower_of.add(self.job)
        self.account1, self.account2, self.account3 = accounts

    def test_save(self):
        self.assertEqual("borsalino", self.job.screen_name)

    def test_query(self):
        self.assertTrue(Job.objects.filter(screen_name="borsalino").exists())

    def test_accounts(self):
        self.assertEqual(self.job.accounts().count(), 2)
        self.assertTrue(
            self.job.accounts().filter(screen_name=self.account1.screen_name).exists()
        )
        self.assertTrue(
            self.job.accounts().filter(screen_name=self.account2.screen_name).exists()
        )
        self.assertFalse(
            self.job.accounts().filter(screen_name=self.account3.screen_name).exists()
        )

    def test_total(self):
        self.assertEqual(self.job.total(), 2)

    def test_percent_over(self):
        self.assertEqual(self.job.percent_over(1.0), (0, 0))
        self.assertEqual(self.job.percent_over(0.9), (0.5, 0.6929646455628166))
        self.assertEqual(self.job.percent_over(0.5), (1, 0))

    def test_save_task(self):
        self.job.save_task("42")
        self.assertEqual(self.job.celery_task_id, "42")
        self.job.save_task(None)
        self.assertIsNone(self.job.celery_task_id)
