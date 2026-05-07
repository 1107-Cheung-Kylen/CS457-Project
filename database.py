from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from sqlalchemy import text
from sqlalchemy import Column, String, Integer, REAL
from sqlalchemy.orm import declarative_base, sessionmaker

url = URL.create(
    drivername="postgresql+psycopg", # specify to use psycopy3 instead of default psycopg2
    username="kylen",
    host="localhost",
    database="database"
)

engine = create_engine(url)

Session = sessionmaker(bind=engine)

Base = declarative_base()