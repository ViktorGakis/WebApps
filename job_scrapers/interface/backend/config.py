from functools import lru_cache
from pathlib import Path
from typing import Callable
from ast import literal_eval
from pydantic_settings import BaseSettings

basedir: Path = Path(__file__).parent
REACT_DIR: Path = basedir.parent / Path('frontend')
REACT_BUILD: Path = REACT_DIR / Path('build')
REACT_TEMPLATE: Path = REACT_BUILD
REACT_STATIC: Path = REACT_BUILD / Path('static')
CWD: Path = Path.cwd()
db_path: Path = CWD / "data" / "scrapers.db"
if not db_path.exists():
    db_path.parent.mkdir(parents=True, exist_ok=True)

def lit_eval(x: str):
    return literal_eval(x.strip()) if isinstance(x,str) else ''


class APISettings(BaseSettings):
    BASE_DIR: Path = basedir
    REACT_PATH: Path = CWD / Path("app/frontend/build")
    STATIC_PATH: Path = REACT_STATIC
    DATA_PATH: Path = CWD / "data"
    FAV_ICON_PATH: Path = REACT_BUILD
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_CONNECT_DICT: dict = {
        "check_same_thread": False
    }  # needed only for sqlite3 compatibility
    debug: bool = True
    debug_exceptions: bool = False
    disable_superuser_dependency: bool = False
    include_admin_routes: bool = False
    title: str = "Job Application Manager"
    TEMPLATES_PATH: Path = REACT_TEMPLATE
    jinja_global_vars: dict[str, Callable] = {}
    jinja_filters: dict[str, Callable] = dict(lit_eval=lit_eval)


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()  # reads variables from environment
