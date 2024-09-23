import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

PROJECT_DIR = Path(__file__).parent.parent
ENV_PATH = Path.joinpath(PROJECT_DIR, 'deployments/.env')
load_dotenv(ENV_PATH)

# TODO: split parameters from string to variable (db_password, db_login, db_name)


@dataclass(frozen=True)
class Config:
    PROJECT_DIR: Path = PROJECT_DIR
    TEMPLATES_DIR: Path = Path.joinpath(PROJECT_DIR, 'src/public')
    DATABASE_URL = os.environ['DATABASE_URL']
    YANDEX_SPELLER_API = os.environ['YANDEX_SPELLER_API']
    YANDEX_SPELLER_API = int(os.environ['MAX_REQUEST_SIZE'])
