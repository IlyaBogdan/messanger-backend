from alembic import command
from os import environ, path
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, drop_database

POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
TESTING = bool(environ.get("TESTING"))
print(TESTING)
POSTGRES_DB = environ.get("POSTGRES_TEST_DB") if TESTING else environ.get("POSTGRES_DB")
print(POSTGRES_DB)
CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

if TESTING:
    create_database(CONNECTION_STRING)
    base_dir = path.dirname(path.dirname(path.dirname(__file__)))
    alembic_cfg = Config(path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        if TESTING:
            drop_database(CONNECTION_STRING)