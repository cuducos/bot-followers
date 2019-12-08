# Bot Followers [![GitHub Actions: Tests](https://github.com/cuducos/bot-followers/workflows/Tests/badge.svg)]() [![GitHub Actions: Black](https://github.com/cuducos/bot-followers/workflows/Black/badge.svg)]()

A web app to check whether followers of a given Twitter account are bots using [Botometer](https://botometer.iuni.iu.edu/). This repository started as a _fork_ of [Twitter
Clean-up](https://github.com/cuducos/twitter-cleanup).

> If you're looking for the CLI version, [it's tagged](https://github.com/cuducos/bot-followers/tree/cli).

## Requirements

* [Twitter API keys](https://developer.twitter.com/apps)
* [Botometer API key](https://market.mashape.com/OSoMe/botometer)
* [Docker Compose](https://docs.docker.com/compose/) for the **development** mode instructions
* [Dokku](http://dokku.viewdocs.io/dokku/) for the **production** mode (deploy) instructions

## Development setup

Copy `.env.sample` as `.env` and fill the environment values as appropriated. I tried to use meaningful variables names, but fell free to [ask](https://github.com/cuducos/bot-followers/issues) if anything is not clear.

To start the services use the default `docker-compose up`.

## Deploy setup

Having a Dokku-ready server, install the following Dokku plug-ins:

* [PostgreSQL](https://github.com/dokku/dokku-postgres-plugin) (or other database of your choice)
* [RabbitMQ](https://github.com/dokku/dokku-rabbitmq-plugin) (or other Celery broker of your choice)
* [Let's Encrypt](https://github.com/dokku/dokku-letsencrypt)

Create an app for Bot Followers in Dokku, add it as a remote repository in your local Git repository, and activate the plug-ins.

For each variable in `.env.sample`, create an equivalent environment variable for your Dokku app.

## Usage

The commands in this section might be prefixed by:

* `docker-compose run --rm django` in **development** mode
* `dokku run <app name>` in **production** mode

### Dashboard

In order to get the app ready, before visiting `/` at your server, you need to run migrations and create a user(s) to access the dashboard.


1. Run migrations with `python manage.py migrate`
1. Create a _super_ user for yourself with `python manage.py createsuperuser`

**It's recommended** to create a proper user to access the dashboard without _super_ powers: all you need to do is to:

1. Login in as _superuser_ create a new user that is _staff_
2. Get back to the _edit_ page of this user
3. In the _Permissions_ menu, add **only** the permission to _view report_ to this new user

### API

There is a simple JSON API at `/api/` to share the report data without the need of user or login.

### Management commands

#### Importing data from the [CLI version](https://github.com/cuducos/bot-followers/tree/cli)

```bash
$ python manage.py import /path/to/borsalino.sqlite3
```

#### Check whether active/inactive jobs are in sync in the dashboard

```bash
$ python manage.py updatecelerytasks
```

#### Empty the queue of pending tasks

```bash
$ python manage.py purgecelerytasks
```

## Contributing

Please, write and run tests, and format your code with [Black](https://github.com/ambv/black):

```bash
$ black .
$ python manage.py test
```
