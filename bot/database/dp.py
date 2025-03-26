from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.database.models import Base

DATABASE_URL = "sqlite:///bot/database/db.sqlite3"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
