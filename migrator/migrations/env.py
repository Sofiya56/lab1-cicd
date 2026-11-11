import os
from alembic import context
from sqlalchemy import create_engine

from app.database import Base
import app.models  # noqa

target_metadata = Base.metadata

engine = create_engine(os.environ["DATABASE_URL"])
with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
