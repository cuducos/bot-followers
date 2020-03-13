from dataclasses import dataclass
from pathlib import Path
from string import ascii_letters, digits
from typing import Iterable, Iterator, Optional
from random import randint

from typer import confirm, echo, prompt, run
from django.utils.crypto import get_random_string  # type: ignore


@dataclass
class Config:
    human_name: str
    name: str
    default: Optional[str] = None

    def value(self, use_default: bool = False):
        if self.default and use_default:
            return self.default

        return prompt(self.human_name, default=self.default)


@dataclass
class Group:
    title: str
    description: str
    configs: Iterable[Config]
    auto_variable: Optional[Iterable[str]] = None

    def __str__(self):
        contents = ("", self.title, f"({self.description})")
        return "\n".join(contents)

    def contents(self, use_defaults: bool = False) -> Iterator[str]:
        settings = {config.name: config.value(use_defaults) for config in self.configs}

        if self.auto_variable:
            name, value, *keys = self.auto_variable
            replacements = tuple(settings[key] for key in keys)
            value = value.format(*replacements)
            settings[name] = value

        for key, value in settings.items():
            yield f"{key}={value}"


@dataclass
class Generator:
    path: Path
    overwrite: bool
    use_defaults: bool
    chars_for_secret_key: str = f"{ascii_letters}{digits}!@#$%^&*(-_=+)"

    @property
    def secret_key(self) -> str:
        return get_random_string(randint(64, 128), self.chars_for_secret_key)

    def __post_init__(self) -> None:
        twitter = Group(
            "Twitter API",
            "You can get yours at https://developer.twitter.com/en/apps",
            (
                Config("API Key", "TWITTER_CONSUMER_KEY"),
                Config("API secret key", "TWITTER_CONSUMER_SECRET"),
                Config("Access token", "TWITTER_ACCESS_TOKEN_KEY"),
                Config("Access token secret", "TWITTER_ACCESS_TOKEN_SECRET"),
            ),
        )
        botometer = Group(
            "Botometer API",
            "You can get yours at https://rapidapi.com/OSoMe/api/botometer",
            (Config("Application Key", "BOTOMETER_MASHAPE_KEY"),),
        )
        django = Group(
            "Django settings",
            "You can find details about them at https://docs.djangoproject.com/3.0/en/topics/settings/",
            (
                Config("Debug mode", "DEBUG", "False"),
                Config("Allowed hosts", "ALLOWED_HOSTS", "127.0.0.1,localhost"),
                Config("Secret key", "SECRET_KEY", self.secret_key),
            ),
        )
        postgres = Group(
            "PostgreSQL credentials",
            "Use the default values for Docker Compose within a developing environment",
            (
                Config("Host", "POSTGRES_HOST", "db"),
                Config("Database name", "POSTGRES_DB", "bot_followers"),
                Config("User name", "POSTGRES_USER", "borsalino"),
                Config("Password", "POSTGRES_PASSWORD", "ehmelhorjair"),
            ),
            (
                "DATABASE_URL",
                "postgres://{}:{}@{}/{}",
                "POSTGRES_USER",
                "POSTGRES_PASSWORD",
                "POSTGRES_HOST",
                "POSTGRES_DB",
            ),
        )
        celery = Group(
            "Celery settings",
            "Use the default values for Docker Compose within a developing environment",
            (Config("Broker URL", "CELERY_BROKER_URL", "amqp://guest:guest@broker//"),),
        )
        cache = Group(
            "Cache",
            "This helps us to avoid unnecessary requests to Botometer API",
            (
                Config(
                    "Number of days to keep results in cache",
                    "CACHE_BOTOMETER_RESULTS_FOR_DAYS",
                    "180",
                ),
            ),
        )
        self.settings: Iterable[Group] = (
            twitter,
            botometer,
            django,
            postgres,
            celery,
            cache,
        )

    def can_write_to_path(self) -> bool:
        if self.overwrite or not self.path.exists():
            return True

        echo(f"There is an existing {self.path.name} file.")
        return confirm("Do you want to overwrite it?")

    def contents(self) -> Iterator[str]:
        for group in self.settings:
            if not self.use_defaults or not all(c.default for c in group.configs):
                echo(group)

            yield f"# {group.title}"
            yield from group.contents(self.use_defaults)
            yield ""

    def __call__(self) -> None:
        if not self.can_write_to_path():
            return

        contents = "\n".join(self.contents())
        self.path.write_text(contents.strip())
        echo(f"{self.path.name} created!")


def main(file_name: str = ".env", overwrite: bool = False, use_defaults: bool = False):
    """Creates a file with the environment variables to run Bot Followers. The
    default file name is .env, but you can change it using --file-name option."""
    Generator(Path(file_name), overwrite, use_defaults)()


if __name__ == "__main__":
    run(main)
