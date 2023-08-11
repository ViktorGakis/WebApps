import logging
from typing import Any, Coroutine, Dict, Optional, Union

from sqlalchemy import Table, inspect, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.future import select

from .async_mode import async_session

log = logging.getLogger(__name__)


def get_primary_key(query_ob):
    return inspect(query_ob).identity


async def update_record(
    model: Union[Table, DeclarativeMeta],
    identifiers: list,
    identifier_field: str,
    field: str,
    value: Any,
    increment: bool = False,
):
    async with async_session.begin() as session:
        if increment:
            # Increment current value
            await session.execute(
                update(model)
                .where(getattr(model, identifier_field).in_(identifiers))
                .values({field: text(f"{field} + {value}")})
            )
        else:
            # Set new value
            await session.execute(
                update(model)
                .where(getattr(model, identifier_field).in_(identifiers))
                .values({field: value})
            )


async def check_attribute_exists(
    db_model: Union[Table, DeclarativeMeta], attribute_name: str, value: Any
) -> bool:
    async with async_session.begin() as session:
        # Check if the attribute exists in the class (optional, for safety)
        if not hasattr(db_model, attribute_name):
            raise ValueError(
                f"'{attribute_name}' is not an attribute of '{db_model.__class__.name}'"
            )

        stmt = select(db_model).filter(getattr(db_model, attribute_name) == value)
        result = await session.execute(stmt)
        instance = result.scalars().first()
        return instance is not None
