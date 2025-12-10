from sqlmodel import Session, create_engine, SQLModel
from pathlib import Path
from sqlalchemy import Engine, event
# Ścieżka do bazy danych w folderze models
db_path = Path(__file__).parent / "database.db"
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create all database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def wipe_database():
    """Drop all tables and recreate them."""
    SQLModel.metadata.drop_all(engine)