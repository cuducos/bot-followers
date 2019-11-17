from time import sleep

import click
from tweepy.error import RateLimitError, TweepError

from bot_followers import BotFollowers


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
        except TweepError as error:
            click.echo(f"\nRestarting due to an error:\n{error}\n")
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
