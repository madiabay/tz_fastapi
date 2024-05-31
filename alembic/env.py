import asyncio
import sys
import os
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncEngine
from sqlalchemy import pool
from alembic import context

# Add path to app in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import models
from app.models import Base
from app.core.config import settings

config = context.config

# Update config database
config.set_main_option('sqlalchemy.url', settings.SQLALCHEMY_DATABASE_URL)

fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
