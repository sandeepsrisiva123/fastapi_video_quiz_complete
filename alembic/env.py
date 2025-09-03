from logging.config import fileConfig
import os, sys
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import Base
from app.models.user import User, RoleEnum
from app.models.refresh_token import RefreshToken
from app.models.video import Video
from app.models.quiz import Quiz, Question, Option

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    config.set_main_option('sqlalchemy.url', DATABASE_URL)

def run_migrations_offline():
    context.configure(url=config.get_main_option('sqlalchemy.url'), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
