from django.shortcuts import resolve_url
from django.test import TestCase
from mixer.backend.django import mixer

from web.core.models import Account, Job


class TestApiView(TestCase):
    def setUp(self):
        self.job = mixer.blend(
            Job, screen_name="Borsalino", image="https://borsalino.png"
        )
        accounts = (
            mixer.blend(Account, botometer=0.62),
            mixer.blend(Account, botometer=0.99),
            mixer.blend(Account, botometer=None),
        )
        for account in accounts:
            account.follower_of.add(self.job)
        self.resp = self.client.get(resolve_url("api"))

    def test_status(self):
        self.assertEqual(200, self.resp.status_code)

    def test_content(self):
        contents = self.resp.json()
        self.assertEqual(1, len(contents["data"]))

        user, *_ = contents["data"]
        expected = {
            "twitter_account": str,
            "image": str,
            "followers": int,
            "analyzed": int,
            "analyzed_percent": float,
            "botometer_over_50": dict,
            "botometer_over_75": dict,
            "botometer_over_80": dict,
            "botometer_over_90": dict,
            "botometer_over_95": dict,
        }
        self.assertEqual(user.keys(), expected.keys())

        for key, obj in expected.items():
            with self.subTest():
                self.assertIsInstance(user[key], obj)
