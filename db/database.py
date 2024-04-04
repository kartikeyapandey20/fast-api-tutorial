from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

DB_HOST = settings.DB_HOST
DB_USER = settings.DB_USER
DB_NAME = settings.DB_NAME
DB_PASS = settings.DB_PASS

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal  = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()