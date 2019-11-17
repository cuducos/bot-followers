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

Usage
-----

Run the CLI within Pipenv's virtualenv:

```bash
$ pipenv shell
$ python -m bot_followers <account handle> <command>
```

Available commands are `analyze` and `report`. For example:

```bash
$ pipenv run python -m bot_followers cuducos analyze
```

Contributing
------------

Please, format your code with [Black](https://github.com/ambv/black).
