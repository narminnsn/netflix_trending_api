import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core import get_db, Base
from app.models import Movie, Season, TVShow, ViewSummary
from datetime import date
import sqlite3

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

def concat_ws(sep, *args):
    return sep.join(str(a) for a in args if a is not None)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        dbapi_connection.create_function("concat_ws", -1, concat_ws)

connection = engine.connect()
transaction = connection.begin()
TestingSessionLocal = sessionmaker(bind=connection, autoflush=False, autocommit=False)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=connection)
    yield
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def db():
    nested = connection.begin_nested()
    session = TestingSessionLocal()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session_, transaction_):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    try:
        movie = Movie(id=1, title="Test Movie", locale="en", release_date=date(2024, 5, 1), runtime=120)
        show = TVShow(id=1, title="Test Show", locale="en")
        season = Season(id=2, tv_show_id=1, season_number=1, release_date=date(2024, 5, 2), runtime=300)
        view1 = ViewSummary(duration="WEEKLY", start_date=date(2025, 6, 2), end_date=date(2025, 6, 8),
                            view_rank=1, hours_viewed=50000000, views=20000000, movie_id=1)
        view2 = ViewSummary(duration="WEEKLY", start_date=date(2025, 6, 2), end_date=date(2025, 6, 8),
                            view_rank=2, hours_viewed=30000000, views=15000000, season_id=2)
        session.add_all([movie, show, season, view1, view2])
        session.commit()

        yield session
    finally:
        session.close()
        nested.rollback()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()