from enum import Flag

from botometer import Botometer, NoTimelineError

from bot_followers.authentication import authentication


BotometerStatus = Flag("BotometerStatus", "PENDING RUNNING READY UNAVAILABLE")


class BotometerResult:
    """Holds Botometer result and avoids repeating the request to their API"""

    def __init__(self, user_id):
        kwargs = authentication.botometer.copy()
        kwargs["wait_on_rate_limit"] = True
        self.botometer = Botometer(**kwargs)

        self.status = BotometerStatus.PENDING
        self._probability = None
        self.user_id = user_id

    def run(self):
        self.status = BotometerStatus.RUNNING
        try:
            result = self.botometer.check_account(self.user_id)
        except NoTimelineError:
            self.status = BotometerStatus.UNAVAILABLE
            self._probability = 0.0  # let's assume it's not a bot
        else:
            self.status = BotometerStatus.READY
            self._probability = result.get("cap", {}).get("universal")

    @property
    def probability(self):
        if self._probability is not None:
            return self._probability

        if self.status is BotometerStatus.PENDING:
            self.run()

        return self._probability
