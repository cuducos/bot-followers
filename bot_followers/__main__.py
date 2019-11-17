from time import sleep

import click
from tweepy.error import RateLimitError

from bot_followers import BotFollowers

import traceback
from os import environ
from sys import exit 

try:
    environ['TWITTER_CONSUMER_KEY']
    environ['TWITTER_CONSUMER_SECRET']
    environ['TWITTER_ACCESS_TOKEN_KEY']
    environ['TWITTER_ACCESS_TOKEN_SECRET'] 
    environ['BOTOMETER_MASHAPE_KEY']
except KeyError:
    print("Environment variable(s) not found")
    print("Please set it using .env file or env VAR=VALUE")
    exit()
     

@click.group()
@click.argument("account")
@click.pass_context
def cli(ctx, account):
    """Bot Follower is a tiny app to check whether followers of a given Twitter
    account are bots."""
    ctx.obj = {"app": BotFollowers(account)}


@cli.command()
@click.pass_context
def analyze(ctx):
    """Run the app to collect & analyze data."""
    while True:
        try:
            ctx.obj.get("app")()
        except RateLimitError:
            click.echo("Due to the Twitter API rate limit, let's take a break…")
            sleep(60 * 5)
            pass
        else:
            break


@cli.command()
@click.pass_context
def report(ctx):
    """Print a simple report of stored results."""
    ctx.obj.get("app").report()


if __name__ == "__main__":
    cli()
