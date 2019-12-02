from botometer import Botometer, NoTimelineError

from web.core.external.authentication import authentication


def botometer(screen_name):
    kwargs = authentication.botometer.copy()
    kwargs["wait_on_rate_limit"] = True
    api = Botometer(**kwargs)

    try:
        result = api.check_account(screen_name)
    except NoTimelineError:
        return 0.5  # user with no post, let's toss a coin

    return result.get("cap", {}).get("universal")
