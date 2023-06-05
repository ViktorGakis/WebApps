from ast import literal_eval
from functools import lru_cache
from pathlib import Path
from typing import Callable

from pydantic import BaseSettings

BASEDIR: Path = Path(__file__).parent
CWD: Path = Path.cwd()

def lit_eval(x: str):
    return literal_eval(x.strip()) if isinstance(x, str) else ""


class APISettings(BaseSettings):
    BASE_DIR: Path = BASEDIR
    STATIC_PATH: Path = BASEDIR / Path("static")
    REACT_PATH: Path = BASEDIR / Path("")
    DATA_PATH: Path = CWD / "data" / "data.json"
    IMGS_PATH: Path = CWD / "data" / "imgs"
    FAV_ICON_PATH: Path = BASEDIR / Path("static") / "favicon.ico"
    debug: bool = True
    debug_exceptions: bool = False
    disable_superuser_dependency: bool = False
    include_admin_routes: bool = False
    title: str = "Test Drive Theoretics"
    TEMPLATES_PATH: Path = BASEDIR / Path("templates")
    jinja_global_vars: dict[str, Callable] = {}
    jinja_filters: dict[str, Callable] = dict(lit_eval=lit_eval)


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()  # reads variables from environment
