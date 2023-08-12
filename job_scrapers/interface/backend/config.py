from functools import lru_cache
from pathlib import Path
from typing import Callable
from ast import literal_eval
from pydantic import BaseSettings

basedir: Path = Path(__file__).parent
workspaceDir: Path = Path.cwd()
db_path: Path = workspaceDir / "data" / "scrapers.db"
if not db_path.exists():
    db_path.parent.mkdir(parents=True, exist_ok=True)

def lit_eval(x: str):
    return literal_eval(x.strip()) if isinstance(x,str) else ''


class APISettings(BaseSettings):
    BASE_DIR: Path = basedir
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{db_path}"
    print(f'{SQLALCHEMY_DATABASE_URI=}')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_CONNECT_DICT: dict = {
        "check_same_thread": False
    }  # needed only for sqlite3 compatibility
    STATIC_PATH: Path = basedir / Path("static")
    debug: bool = True
    debug_exceptions: bool = False
    disable_superuser_dependency: bool = False
    include_admin_routes: bool = False
    title: str = "Job Application Manager"
    TEMPLATES_PATH: Path = basedir / Path("templates")
    jinja_global_vars: dict[str, Callable] = {}
    jinja_filters: dict[str, Callable] = dict(lit_eval=lit_eval)


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()  # reads variables from environment
