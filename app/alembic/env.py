import os
import sys
import pathlib
import importlib

from logging.config import fileConfig

from dotenv import load_dotenv
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from const.const import DATABASE_URL_ALEMBIC

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

models_path = BASE_DIR / "models"

for model_file in models_path.glob("*.py"):
    if model_file.name.startswith("_") or model_file.name == "__init__.py":
        continue
    module_name = f"models.{model_file.stem}"
    importlib.import_module(module_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL_ALEMBIC,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL_ALEMBIC,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
