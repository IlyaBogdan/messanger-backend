import os
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database

os.environ['TESTING'] = 'True'

from database import CONNECTION_STRING

print('Creating test database...')
create_database(CONNECTION_STRING)
print('Database created.')
base_dir = os.path.dirname(__file__)
alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
command.upgrade(alembic_cfg, "head")

@pytest.fixture(scope="session", autouse=True)
def get_db():
    try:
        yield
    finally:
        print('Dropping test database...')
        #drop_database(CONNECTION_STRING)
        print('Database dropped.')