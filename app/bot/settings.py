import os

from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Bots:
    tg_token: str
    admin_id: int

@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    load_dotenv(path)
    return Settings(
        bots=Bots(
            tg_token=str(os.getenv("TG_TOKEN")),
            admin_id=int(os.getenv("ADMIN_ID"))
        )
    )

settings = get_settings('.env')