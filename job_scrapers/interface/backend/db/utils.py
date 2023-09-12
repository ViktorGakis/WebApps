from typing import Any, Coroutine, Dict, List, Optional, Tuple, Union

from sqlalchemy import Table, and_, inspect, not_, or_, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .async_mode import async_session

OPERATORS_MAP = {
    "==": lambda attr, value: attr == value,
    "!=": lambda attr, value: attr != value,
    ">": lambda attr, value: attr > value,
    "<": lambda attr, value: attr < value,
    ">=": lambda attr, value: attr >= value,
    "<=": lambda attr, value: attr <= value,
    "in": lambda attr, value: attr.in_(value)
    if isinstance(value, list)
    else attr.in_([value]),
    "not_in": lambda attr, value: ~attr.in_(value)
    if isinstance(value, list)
    else ~attr.in_([value]),
    "like": lambda attr, value: attr.like(value),
    "ilike": lambda attr, value: attr.ilike(value),
    "is": lambda attr, value: attr.is_(value),
    "not_is": lambda attr, value: ~attr.is_(value),
}


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


async def save_records(records):
    async with async_session.begin() as ses:
        ses.add_all(records)
        await ses.commit()


async def update_record_from_dict(records, dict_list: List[dict[str, Any]]):
    for record, attr_dict in zip(records, dict_list):
        for k, v in attr_dict.items():
            setattr(record, k, v)
    await save_records(records)


async def create_record(record_model, *args, **kwds):
    record = record_model(*args, **kwds)
    await save_records([record])
    return record


async def get_records(
    model,
    conditions: List[Tuple[str, str, Union[Any, List[Any]]]],
    logical_operator: str = "AND",
):
    async with async_session.begin() as session:
        query = select(model)
        filters = []

        for attrib, op, value in conditions:
            if op not in OPERATORS_MAP:
                raise ValueError(f"Unsupported operator: {op}")
            filter_condition = OPERATORS_MAP[op](getattr(model, attrib), value)
            filters.append(filter_condition)

        if logical_operator.upper() == "AND":
            query = query.where(and_(*filters))
        elif logical_operator.upper() == "OR":
            query = query.where(or_(*filters))
        elif logical_operator.upper() == "NOT":
            query = query.where(not_(*filters))
        else:
            raise ValueError("Logical operator must be 'AND', 'OR', or 'NOT'")

        result = await session.execute(query)
        return list(result.scalars())
