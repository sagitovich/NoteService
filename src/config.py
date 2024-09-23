import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()


@dataclass(frozen=True)
class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    YANDEX_SPELLER_API = os.getenv('YANDEX_SPELLER_API')
    MAX_REQUEST_SIZE = int(os.getenv('MAX_REQUEST_SIZE'))
