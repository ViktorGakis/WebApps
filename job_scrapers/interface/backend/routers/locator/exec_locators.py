from job_seeker import locator_gmap, locator_nom, locator_gmap_args, locator_nom_args


from logging import Logger
from pprint import pformat
from typing import Optional

from pydantic import BaseModel, Extra, ValidationError, validator


from ...logger import logdef

log: Logger = logdef(__name__)


class ExecArgsMaps(BaseModel):
    """
    locator_gmap exec vars API
    """

    chunk_size: Optional[int] = locator_gmap_args['chunk_size']['options']['9']
    limit: Optional[int] = locator_gmap_args['limit']['options']['5']

    class Config:
        extra: Extra = Extra.forbid

    @validator("*",  pre=True)
    def chunk_val(cls, v, field):
        return field.default if (v == "" or v is None) else v


class ExecArgsNom(BaseModel):
    """
    locator_gmap exec vars API
    """

    mode: Optional[str] = locator_nom_args['mode']['options']['rev']

    class Config:
        extra: Extra = Extra.forbid

    @validator("*",  pre=True)
    def chunk_val(cls, v, field):
        return field.default if (v == "" or v is None) else v


async def parse_locator_map_args(rq_args: dict) -> ExecArgsMaps | None:
    try:
        return ExecArgsMaps.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())


async def parse_locator_nom_args(rq_args: dict) -> ExecArgsNom | None:
    try:
        return ExecArgsNom.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())