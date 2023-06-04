from ast import literal_eval
from functools import lru_cache
from pathlib import Path
from typing import Callable

from pydantic import BaseSettings

basedir: Path = Path(__file__).parent


def lit_eval(x: str):
    return literal_eval(x.strip()) if isinstance(x, str) else ""


class APISettings(BaseSettings):
    BASE_DIR: Path = basedir
    STATIC_PATH: Path = basedir / Path("static")
    FAV_ICON_PATH: Path = basedir / Path("static") / 'favicon.ico'
    debug: bool = True
    debug_exceptions: bool = False
    disable_superuser_dependency: bool = False
    include_admin_routes: bool = False
    title: str = "Test Drive Theoretics"
    TEMPLATES_PATH: Path = basedir / Path("templates")
    jinja_global_vars: dict[str, Callable] = {}
    jinja_filters: dict[str, Callable] = dict(lit_eval=lit_eval)


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()  # reads variables from environment
