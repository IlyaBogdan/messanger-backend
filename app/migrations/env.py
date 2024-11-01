from __future__ import with_statement
from alembic import context
from sqlalchemy import create_engine
from logging.config import fileConfig

from database import CONNECTION_STRING
from database import Base
import modules.v1.models.user
import modules.v1.models.chat
import modules.v1.models.chat_event
import modules.v1.models.message
import modules.v1.models.attachment

config = context.config
target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    context.configure(
        url=CONNECTION_STRING, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = create_engine(CONNECTION_STRING)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
