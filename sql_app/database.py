import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL,echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=True,bind=engine)

Base = declarative_base()