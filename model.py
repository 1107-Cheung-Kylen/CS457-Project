from sqlalchemy import select
from sqlalchemy import Column, String, Integer, REAL, SmallInteger, Date
from sqlalchemy.orm import declarative_base

from database import Session # avoid rewriting connection code from database.py

from datetime import date

from tabulate import tabulate

# sessionUsers = Session()

Base = declarative_base()

class Cities(Base):
    __tablename__ = 'cities'
    __table_args__ = {'schema': 'project'}

    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    lat = Column(REAL)
    lng = Column(REAL)
    population = Column(Integer)
    country_id = Column(SmallInteger)
    admin_id = Column(SmallInteger)

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'project'}

    name = Column(String)
    email = Column(String)
    id = Column(Integer, primary_key=True)

class User_Cities(Base):
    __tablename__ = 'user_cities'
    __table_args__ = {'schema': 'project'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    city_id = Column(Integer)
    date = Column(Date)
    rating_food = Column(SmallInteger)
    rating_shopping = Column(SmallInteger)
    rating_recreation = Column(SmallInteger)

class Admin_Regions(Base):
    __tablename__ = 'admin_regions'
    __table_args__ = {'schema': 'project'}

    admin_name = Column(String)
    country_id = Column(SmallInteger)
    admin_id = Column(SmallInteger, primary_key=True)

class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = {'schema': 'project'}

    country_name = Column(String)
    country_id = Column(SmallInteger, primary_key=True)

# new_user = Users(name = "Alice", email = "aliceg@unr.edu")

test_date = date(2026, 5, 3)
new_user_city = User_Cities(user_id = 1, city_id = 1392685764, date = test_date, rating_food = 4, rating_shopping = 5, rating_recreation = 2)

# with Session() as session:
#     session.add(new_user)
#     session.commit()

def select_user():
    # access database and list all
    with Session() as session:
        # statement = select(Users.name)
        # users_name = session.execute(statement).scalars().all() # returns a list
        # print(users_name)

        # users_name = session.scalars(select(Users.name)).all()

        users_tuple = session.execute(select(Users.name, Users.email, Users.id)).all()

        for index, (name, email, id) in enumerate(users_tuple):
            print(f"{index + 1}: {name}, {email}") # use f-string

        input_choice = int(input("pick a user: "))
        input_name, input_email, input_id = users_tuple[input_choice - 1] # subtract 1 since array starts at 0
        # print(input_name)

        # users_id = session.scalars(select(Users.id).where(Users.name == input_name) & (Users.email == input_email)).all()
        print(f"Selected {input_name}")
        return input_id
    
        session.close()

def view_cities(user):
    print("Viewing Cities")
    
    print(user)
    # use SQLalchamey (do NOT load entire database into array)
    with Session() as session:
        # session.add(new_user_city)
        # session.commit()

        # cities = session.execute(select(Cities, Admin_Regions, Countries).join(User_Cities, Cities.id == User_Cities.city_id).join(Admin_Regions, Cities.admin_id == Admin_Regions.admin_id).join(Countries, Cities.country_id == Countries.country_id).where(User_Cities.user_id == user)).all()

        cities = session.execute(
            select(Cities.city_name, Admin_Regions.admin_name, Countries.country_name, Cities.lat, Cities.lng, Cities.population, User_Cities.date, User_Cities.rating_food, User_Cities.rating_recreation, User_Cities.rating_shopping)
            .join(User_Cities, Cities.id == User_Cities.city_id)
            .join(Admin_Regions, Cities.admin_id == Admin_Regions.admin_id)
            .join(Countries, Cities.country_id == Countries.country_id)
            .where(User_Cities.user_id == user)
            # maybe need another where clause for admin region?
        ).all()

        # cities_id = []
        # for city_id in cities_id:
        #     cities_id.append(city_id)
        
        
        # print(cities[0].city_id)

    view_city_headers = [
        "City", "State/Province/Region", "Country", "Lat", "Lng", "Population", "Date Visited", "Food", "Recreation", "Shopping",
    ]

    print(tabulate(cities, headers=view_city_headers, tablefmt="grid"))

    # for city in cities:
    #     print(f"{city.city_name}, {city.lat}, {city.lng}, {city.admin_name}, {city.country_name}")

    # for city_name, region_name, country_name in cities: # cities is a ROW object
    #     print(city_name, region_name, country_name)