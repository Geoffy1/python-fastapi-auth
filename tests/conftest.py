import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.core.config import settings
from app.db.session import SessionLocal


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="module")
def db_engine():
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
yield engine
Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
TestingSessionLocal = sessionmaker(autocommi