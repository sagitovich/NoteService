import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

PROJECT_DIR = Path(__file__).parent.parent
ENV_PATH = Path.joinpath(PROJECT_DIR, 'deployments/.env')
load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class Config:
    PROJECT_DIR: Path = PROJECT_DIR
    TEMPLATES_DIR: Path = Path.joinpath(PROJECT_DIR, 'src/public')
    YANDEX_SPELLER_API = os.environ['YANDEX_SPELLER_API']
    MAX_REQUEST_SIZE = int(os.environ['MAX_REQUEST_SIZE'])
    SECRET_KEY = os.environ['SECRET_KEY']

    DATABASE_BASE_URL = os.environ['DATABASE_BASE_URL']
    DATABASE_USER = os.environ['DATABASE_USER']
    DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
    DATABASE_HOST = os.environ['DATABASE_HOST']
    DATABASE_NAME = os.environ['DATABASE_NAME']

    DATABASE_URL = DATABASE_BASE_URL.format(DATABASE_USER, DATABASE_PASSWORD, 
                            DATABASE_HOST, DATABASE_NAME)
