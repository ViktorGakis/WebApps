from logging import Logger

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
import sqlalchemy.event
import sqlalchemy.exc
import sqlalchemy.orm
import sqlalchemy.pool
from sqlalchemy import and_, func, or_, select, update, cast, DateTime, type_coerce

from ..logger import logdef
from . import base, models
from .async_mode import Session, async_session, engine, get_ses
from .paginator import Pagination, paginate
from .sync import engineSync, SessionLocalSync
from .utils import get_primary_key, create_objs, retrieve_objs, update_objs, obj_retriever, update_record

log: Logger = logdef(__name__)

Base = base.Base


async def init() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("Db initialized.")


async def disc() -> None:
    await engine.dispose()
    log.info("Db closed.")
    log.info("Db closed.")
