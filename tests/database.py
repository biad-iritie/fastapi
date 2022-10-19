from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from app.main import app
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format("postgres",
                                                               "admin",
                                                               "localhost",
                                                               "5432",
                                                               "fastapi_test")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()

# Dependency


""" def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() """


#app.dependency_overrides[get_db] = override_get_db

#client = TestClient(app)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # if I use alembic
    # command.downgrade("base")
    # command.upgrade("head")
    # run our code before we run our test
    yield TestClient(app)
    # run our code after we run our test finishes
