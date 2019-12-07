from functools import partial


class JobSerializer:
    def json(self):
        serialized = {
            "twitter_account": self.screen_name,
            "followers": self.total_followers,
            "analyzed": self.followers.analyzed().count(),
            "analyzed_percent": None,
            "botometer_over_50": None,
            "botometer_over_75": None,
            "botometer_over_80": None,
            "botometer_over_90": None,
            "botometer_over_95": None,
        }

        if not self.total_followers or not self.followers.analyzed().exists():
            return serialized

        def wrapper(percent, error):
            return {"percent": percent, "error": error}

        percent_over = partial(self.percent_over, wrapper=wrapper)
        botometer = {
            "analyzed_percent": serialized["analyzed"] / serialized["followers"],
            "botometer_over_50": percent_over(0.5, over_or_equal=False),
            "botometer_over_75": percent_over(0.75),
            "botometer_over_80": percent_over(0.8),
            "botometer_over_90": percent_over(0.9),
            "botometer_over_95": percent_over(0.95),
        }
        serialized.update(botometer)
        return serialized
