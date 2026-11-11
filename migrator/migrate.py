import os
import sys
import time

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

url = os.environ["DATABASE_URL"]

for attempt in range(1, 31):
    try:
        with create_engine(url).connect() as conn:
            conn.execute(text("SELECT 1"))
        break
    except Exception as exc:
        print(f"DB not ready ({attempt}/30): {exc}", flush=True)
        time.sleep(3)
else:
    sys.exit(1)

command.upgrade(Config("migrator/alembic.ini"), "head")
print("Migrations applied", flush=True)