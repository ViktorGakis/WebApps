import logging
from typing import Any, Coroutine, Dict, Optional, Union

from sqlalchemy import Table, inspect, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .async_mode import async_session

log = logging.getLogger(__name__)


def get_primary_key(query_ob):
    return inspect(query_ob).identity


def valid_model_attributes(
    model: DeclarativeMeta, attribute_dict: Dict[str, Any]
) -> bool:
    if not attribute_dict:
        log.error("attribute_dict must not be empty.")
        return False

    if invalid_attributes := [
        k for k, _ in attribute_dict.items() if not hasattr(model, k)
    ]:
        log.error(
            f"The following attributes do not exist in the model: {', '.join(invalid_attributes)}"
        )
        return False

    return True


async def create_objs(model, attribute_dicts):
    # Initialize an empty list to hold the instances of the model class
    instances = []

    for attribute_dict in attribute_dicts:
        if not valid_model_attributes(model, attribute_dict):
            continue

        # Create a new object of the model class
        ob = model(**attribute_dict)

        # Add the instance to the instances list
        instances.append(ob)

    # Use the already setup async session from db module
    async with async_session.begin() as session:
        # Add all instances to the session at once
        session.add_all(instances)

        # Flush so that we get the primary keys
        await session.flush()

        # Commit the changes
        await session.commit()

    # Get the primary keys of the newly persisted objects
    primary_keys = [get_primary_key(ob) for ob in instances]

    # Return the list of primary keys
    return primary_keys


async def retrieve_obj_helper(
    session: AsyncSession, model: DeclarativeMeta, primary_key
):
    return await session.get(model, primary_key)


async def retrieve_objs(
    primary_keys: list[Any],
    model: DeclarativeMeta,
) -> list:
    query_objs = []
    async with async_session.begin() as session:
        query_objs = [
            await retrieve_obj_helper(session, model, pkey) for pkey in primary_keys
        ]

        if query_objs is None:
            log.error(f"No objects found with primary key {primary_keys}.")

        return query_objs


async def modify_obj(query_obj, column_value_dict: Dict[str, Any]):
    # Modify the object
    for column, new_value in column_value_dict.items():
        if getattr(query_obj, column) != new_value:
            setattr(query_obj, column, new_value)


async def update_objs(
    primary_keys: list,
    model: DeclarativeMeta,
    column_value_dicts: list[Dict[str, Any]],
) -> Coroutine[Any, Any, None]:
    for column_value_dict in column_value_dicts:
        if not valid_model_attributes(model, column_value_dict):
            return

    query_objs = await retrieve_objs(primary_keys, model)

    # Use the already setup async session from db module
    if query_objs:
        async with async_session.begin() as session:
            for obj, column_value_dict in zip(query_objs, column_value_dicts):
                session.add(obj)
                await modify_obj(obj, column_value_dict)
            # Commit the changes
            await session.commit()
    else:
        log.debug("Object not found.")


async def obj_retriever(model, column, identifiers):
    async with async_session() as session:
        query = await session.execute(
            select(model).where(getattr(model, column).in_(identifiers))
        )
        return query.scalars().all()


async def update_record(
    model: Union[Table, DeclarativeMeta],
    identifiers: list,
    identifier_field: str,
    field: str,
    value: Any,
    increment: bool = False,
):
    async with async_session() as session:
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
        await session.commit()
