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

# with engine.connect() as connection:
#     result = connection.execute(text("SELECT * FROM project.cities LIMIT 100;"))
#     for row in result:
#         print(row)

class Cities(Base):
    __tablename__ = 'cities'
    __table_args__ = {'schema': 'project'}

    city = Column(String)
    city_ascii = Column(String)
    lat = Column(REAL)
    lng = Column(REAL)
    country = Column(String)
    iso2 = Column(String(2))
    iso3 = Column(String(3))
    admin_name = Column(String)
    capital = Column(String)
    population = Column(Integer)
    id = Column(Integer, primary_key=True)


with Session() as session:
    # examples of using sqlalchemy to query database

    # filter by city name, and return cities called "New York"
    result = session.query(Cities).filter(Cities.city == "New York")

    for row in result:
        print(row.lng)

session.close()