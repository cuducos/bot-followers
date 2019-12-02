from dataclasses import dataclass

from tweepy import API, Cursor

from web.core.external.authentication import authentication


@dataclass
class Twitter:
    screen_name: str

    def __post_init__(self):
        self.api = API(authentication.tweepy, wait_on_rate_limit=True)
        self.target = self.api.get_user(self.screen_name)

        # shortcuts
        self.screen_name = self.target.screen_name
        self.total_followers = self.target.followers_count

    @property
    def followers(self):
        cursor = Cursor(self.api.followers, screen_name=self.screen_name)
        yield from (user for user in cursor.items() if not user.protected)
