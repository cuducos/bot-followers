# Bot Follower

A web app to check whether followers of a given Twitter account are bots.
This code is a _fork_ of [Twitter
Clean-up](https://github.com/cuducos/twitter-cleanup). 

## Requirements

* [Docker Compose](https://docs.docker.com/compose/)
* [Twitter API keys](https://developer.twitter.com/apps)
* [Botometer API key](https://market.mashape.com/OSoMe/botometer)

## Setup

Copy `.env.sample` as `.env` and fill the environment values as necessary. I tried to use meaningful variables names, but fell free to ask here if anything is not clear.
 
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

Now access [`localhost:8000`](http://localhost:8000) and create a proper user to access the web app without _super_ powers: all you need to do is to add just the permission to _view job_ in the Django Admin interface.

### Importing data from the (old) CLI version

There's a command to import data generated in the CLI, the `.sqlite3` generated files:

```bash
$ docker-compose run --rm django python manage.py import /path/to/borsalino.sqlite3
```

## Contributing

Please, format your code with [Black](https://github.com/ambv/black).