from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "sqlite:///./database.sqlite"

engine = create_engine(database_url,
                            native_datetime = True,
                                connect_args = {
                                    "check_same_thread": False
                                }
                            )

SessionLocal = sessionmaker( bind = engine,
                            autocommit = False,
                            autoflush = False
                            )

Base = declarative_base()
