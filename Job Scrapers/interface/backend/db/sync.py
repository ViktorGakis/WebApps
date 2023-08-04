from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from ..config import get_api_settings

settings = get_api_settings()

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
engineSync: Engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args=settings.SQLALCHEMY_DATABASE_CONNECT_DICT
)
SessionLocalSync: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engineSync)

Base = declarative_base()