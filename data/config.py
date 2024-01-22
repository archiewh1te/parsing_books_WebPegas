from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBot:
    token: str
    admins_id: list[int]


@dataclass
class Config:
    tg_bot: TelegramBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TelegramBot(
            token=env.str("BOT_TOKEN"),
            admins_id=list(map(int, env.list("ADMINS"))),

        )
    )
