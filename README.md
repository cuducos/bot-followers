# Bot Followers [![GitHub Actions: Tests workflow](https://github.com/cuducos/bot-followers/workflows/Tests/badge.svg)]() [![GitHub Actions: Black workflow](https://github.com/cuducos/bot-followers/workflows/Black/badge.svg)]() 

A web app to check whether followers of a given Twitter account are bots using [Botometer](https://botometer.iuni.iu.edu/). This repository started as a _fork_ of [Twitter
Clean-up](https://github.com/cuducos/twitter-cleanup).

> If you're looking for the CLI version, [it's tagged](https://github.com/cuducos/bot-followers/tree/cli). 

## Requirements

* [Docker Compose](https://docs.docker.com/compose/)
* [Twitter API keys](https://developer.twitter.com/apps)
* [Botometer API key](https://market.mashape.com/OSoMe/botometer)

## Setup

Copy `.env.sample` as `.env` and fill the environment values as apropriated. I tried to use meaningful variables names, but fell free to [ask](https://github.com/cuducos/bot-followers/issues) if anything is not clear.
 
## Running

First, we need to run migrations:

```bash
$ docker-compose run --rm django python manage.py migrate
```

Then we need to collect statics:

```bash
$ docker-compose run --rm django python manage.py collectstatics --noinput
```

Finally, create a _super_ user for yourself:

```bash
$ docker-compose run --rm django python manage.py createsuperuser
```

### Dashboard

You can access a dashboard to control the app at  [`localhost:8000`](http://localhost:8000).

**It's recommended** that you create a proper user to access the web app without _super_ powers: all you need to do is to:
1. Login in as _superuser_ create a new user that is _staff_
2. In the _Permissions_ menu, add just the permission to _view report_ to this new user

### API

There isa simple API to share the results without the need of user or login: [`localhost:8000/api/`](http://localhost:8000/api/).

### Commands

#### Importing data from the (old) CLI version

```bash
$ docker-compose run --rm django python manage.py import /path/to/borsalino.sqlite3
```

#### Check whether active/inactive jobs are in sync with reality

```bash
$ docker-compose run --rm django python manage.py updatecelerytasks
```

#### Empty the queue of pending tasks

```bash
$ docker-compose run --rm django python manage.py purgecelerytasks
```

## Contributing

Please, write and run tests, and format your code with [Black](https://github.com/ambv/black):

```bash
$ black .
$ python manage.py test
```
