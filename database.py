from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# export DB_URL='postgresql://username:password@localhost:5432/dbname'
# export DB_URL='postgresql://postgres:B4D455@localhost:5432/enerbit'
DB_URL = os.environ.get('DB_URL')


if DB_URL is not None:
    print('Error: The database URL is not set in the environment')


engine = create_engine(DB_URL)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

