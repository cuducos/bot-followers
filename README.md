Bot Follower
================

Tiny script to check whether followers of a given Twitter account are bots.
This code is a _fork_ of [Twitter
Clean-up](https://github.com/cuducos/twitter-cleanup). 

Requirements
------------

[Python](https://python.org) 3.8, [Pipenv](https://pipenv.readthedocs.io/en/latest/) and environment variables with your [Twitter API keys](https://developer.twitter.com/apps) and with [Botometer API key](https://market.mashape.com/OSoMe/botometer):

  * ``TWITTER_CONSUMER_KEY``
  * ``TWITTER_CONSUMER_SECRET``
  * ``TWITTER_ACCESS_TOKEN_KEY``
  * ``TWITTER_ACCESS_TOKEN_SECRET``
  * ``BOTOMETER_MASHAPE_KEY``

The Botometer API key is created when you create a new app in the [RapidAPI dashboard](https://rapidapi.com/developer/new).

Usage
-----

Run the CLI within Pipenv's virtualenv:

```bash
$ pipenv shell
$ python -m bot_followers <account handle> <command>
```

Available commands are `analyze` and `report`. For example:

```bash
$ pipenv run python -m bot_followers borsalino analyze
```

After a while, you can check a report (even before `analyze` command has finish its job):

```
$ run python -m bot_followers borsalino analyze

Analysis of @borsalino's followers

Total followers..................: 5,441,059
Followers analyzed...............: 4,380
Percentage analyzed..............: 0.08%

Accounts with +50% in Botometer..: 25.37% (±1.29%)
Accounts with +75% in Botometer..: 18.56% (±1.15%)
Accounts with +80% in Botometer..: 13.68% (±1.02%)
Accounts with +90% in Botometer..: 9.2% (±0.86%)
Accounts with +95% in Botometer..: 1.16% (±0.32%)
```

Contributing
------------

Please, format your code with [Black](https://github.com/ambv/black).