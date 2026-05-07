from sqlalchemy import select
from sqlalchemy import func # used for lowercase city matching
from sqlalchemy import Column, String, Integer, REAL, SmallInteger, Date # used in classes for data type
from sqlalchemy.orm import declarative_base

from database import Session # avoid rewriting connection code from database.py

from datetime import date, datetime

from tabulate import tabulate

import sys

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

def select_user():
    print("Select a user (or create one!)")

    # access database and list all
    with Session() as session:
        users_tuple = session.execute(select(Users.name, Users.email, Users.id)).all()
    
    users_num = len(users_tuple)

    for index, (name, email, id) in enumerate(users_tuple):
        print(f"{index + 1}: {name}, {email}") # use f-string
    
    print(f"{users_num + 1}: Add User")
    print(f"{users_num + 2}: Remove User")
    print(f"{users_num + 3}: Exit Program")

    input_choice = float('inf') # set input_choice to be +infinity
    # use while loop to make sure valid user is picked
    while input_choice < 1 or input_choice > users_num + 3:
        input_choice = int(input("Pick an option: "))
    
    if input_choice == (users_num + 1):
        # input_choice = float('-inf')
        add_user()
        select_user()
        return
        # print("Add USER")
    elif input_choice == (users_num + 2):
        remove_user()
        select_user()
        return
    elif input_choice == (users_num + 3):
        sys.exit()

    input_name, input_email, input_id = users_tuple[input_choice - 1] # subtract 1 since array starts at 0

    # users_id = session.scalars(select(Users.id).where(Users.name == input_name) & (Users.email == input_email)).all()
    print(f"{input_name}'s City Tracker")
    
    return input_id

    # session.close()

def add_user():
    user_name = input("Enter a name: ")
    user_email = input("Enter an email: ")
    new_user = Users(name = user_name, email = user_email)

    with Session() as session:
        session.add(new_user)
        session.commit()

def remove_user():
    with Session() as session:
        users_tuple = session.execute(select(Users.name, Users.email, Users.id)).all()
    
    users_num = len(users_tuple)

    for index, (name, email, id) in enumerate(users_tuple):
        print(f"{index + 1}: {name}, {email}") # use f-string
    print(f"{users_num + 1}: Exit Program")

    # input_choice = int(input("Pick a user to remove: "))

    input_choice = float('inf')
    while input_choice < 1 or input_choice > users_num + 2:
        input_choice = int(input("Select a user to remove: "))
    if input_choice == (users_num + 1):
        sys.exit()

    name, email, id = users_tuple[input_choice - 1]
    print(name)

    with Session() as session: 
        # get row to delete
        user_delete = session.execute(select(Users).where(Users.id == id)).scalar()
        if user_delete:
            session.delete(user_delete)
            session.commit()

        # need to remove cities from user_cities table too
        cities_delete = session.execute(select(User_Cities).where(User_Cities.user_id == id)).scalars()
        
        if cities_delete:
            for city_delete in cities_delete:
                session.delete(city_delete)
            session.commit()

def remove_cities(user):
    with Session() as session:
        cities = session.execute(
            select(Cities.city_name, Admin_Regions.admin_name, Countries.country_name, Cities.lat, Cities.lng, Cities.population, User_Cities.date, User_Cities.rating_food, User_Cities.rating_shopping, User_Cities.rating_recreation, User_Cities.id)
            .join(User_Cities, Cities.id == User_Cities.city_id)
            .join(Admin_Regions, Cities.admin_id == Admin_Regions.admin_id)
            .join(Countries, Cities.country_id == Countries.country_id)
            .where(User_Cities.user_id == user)
            # maybe need another where clause for admin region?
        ).all()

    view_city_headers = [
        "City", "State/Province/Region", "Country", "Lat", "Lng", "Population", "Date Visited (Year, Month, Day)", "Food", "Shopping", "Recreation",
    ]

    cities_tabulate = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]] for row in cities]
    print(tabulate(cities_tabulate, headers=view_city_headers, tablefmt="grid", showindex=range(1, len(cities) + 1)))

    input_choice = float('inf')
    while input_choice < 1 or input_choice > (len(cities)):
        input_choice = int(input("Enter the number of the city to remove: "))
    city = cities[input_choice - 1]

    with Session() as session:
        city_delete = session.execute(select(User_Cities).where(User_Cities.id == city.id)).scalar()

    if city_delete:
        session.delete(city_delete)
        session.commit()


def view_cities(user):
    # print("Viewing Cities")
    
    # print(user)
    # use SQLalchamey (do NOT load entire database into array)
    with Session() as session:
        # session.add(new_user_city)
        # session.commit()

        # cities = session.execute(select(Cities, Admin_Regions, Countries).join(User_Cities, Cities.id == User_Cities.city_id).join(Admin_Regions, Cities.admin_id == Admin_Regions.admin_id).join(Countries, Cities.country_id == Countries.country_id).where(User_Cities.user_id == user)).all()

        cities = session.execute(
            select(Cities.city_name, Admin_Regions.admin_name, Countries.country_name, Cities.lat, Cities.lng, Cities.population, User_Cities.date, User_Cities.rating_food, User_Cities.rating_shopping, User_Cities.rating_recreation)
            .join(User_Cities, Cities.id == User_Cities.city_id)
            .join(Admin_Regions, Cities.admin_id == Admin_Regions.admin_id)
            .join(Countries, Cities.country_id == Countries.country_id)
            .where(User_Cities.user_id == user)
            # maybe need another where clause for admin region?
        ).all()

    view_city_headers = [
        "City", "State/Province/Region", "Country", "Lat", "Lng", "Population", "Date Visited (Year, Month, Day)", "Food", "Shopping", "Recreation",
    ]

    print(tabulate(cities, headers=view_city_headers, tablefmt="grid"))

def add_cities(user):
    # print("Adding City")

    while True:
        user_city = input("Enter a city name (try to be exact): ")

        # use SQLAlchemy to get exact city ID
        with Session() as session:
            statement = select(Cities.city_name, Cities.id, Admin_Regions.admin_name, Countries.country_name).join(Admin_Regions, Cities.admin_id == Admin_Regions.admin_id).join(Countries, Cities.country_id == Countries.country_id).where(func.lower(Cities.city_name) == func.lower(user_city))
            user_cities = session.execute(statement).all() # user_cities returns a list along with boolean (True if empty, false if not empty)
        
        if user_cities: # if user_cities returned a true, break out of while loop
            break
        else:
            print("No matching cities found. Try again")

    # need logic to select from array of user cities, also ignore capitalization
    for index, (city_name, city_id, admin_name, country_name) in enumerate(user_cities):
        print(f"{index + 1}. {city_name}, {admin_name}, {country_name}")
    
    user_filtered_city = float('inf')
    while user_filtered_city < 1 or user_filtered_city > (len(user_cities)):
        user_filtered_city = int(input("Select a city: "))

    # allow user to choose exact city (city, state, country)
    city = user_cities[user_filtered_city - 1]
    city_id = city.id # get city ID

    # convert user_date_input (string) into user_date (date object)
    while True:
        user_date_input = input("Enter a date (ex. '2026-05-03' for May 3, 2026): ")
        try:
            user_date = datetime.strptime(user_date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid format!")

    user_food = 6
    user_shopping = 6
    user_recreation = 6
    while user_food > 5:
        user_food = int(input("Enter a food rating (1-5): "))
    while user_shopping > 5:
        user_shopping = int(input("Enter a shopping rating (1-5): "))
    while user_recreation > 5:
        user_recreation = int(input("Enter a recreation rating (1-5): "))

    # create city object
    user_city = User_Cities(user_id = user, city_id = city_id, date = user_date, rating_food = user_food, rating_shopping = user_shopping, rating_recreation = user_recreation)

    user_city_tabulate = [[city.city_name, city.admin_name, city.country_name, user_date, user_food, user_shopping, user_recreation]]

    add_city_headers = [
        "City", "State/Province/Region", "Country", "Date Visited (Year, Month, Day)", "Food", "Shopping", "Recreation",
    ]

    print(tabulate(user_city_tabulate, headers=add_city_headers, tablefmt="grid"))

    input_choice = input(f"Add {city.city_name} to visited cities? (Y/N): ")
    if input_choice == "Y":
        with Session() as session:
            session.add(user_city) # automatically adds to User_City table since object is a user_city type
            session.commit()
    else:
        return