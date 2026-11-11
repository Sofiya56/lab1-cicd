import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from app.database import Base, engine
import app.models  # noqa


@pytest.fixture(autouse=True, scope="session")
def _schema():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
