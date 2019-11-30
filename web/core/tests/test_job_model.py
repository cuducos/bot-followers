from django.test import TestCase

from web.core.models import Job


class TestJobModel(TestCase):
    def setUp(self):
        self.job = Job.objects.create(screen_name="Borsalino")

    def test_save(self):
        self.assertEqual("borsalino", self.job.screen_name)

    def test_query(self):
        self.assertTrue(Job.objects.filter(screen_name="borsalino").exists())
