# database connection
# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL

# url = URL.create(
#     drivername="postgresql+psycopg",
#     username="kylen",
#     host="localhost",
#     database="database"
# )

# engine = create_engine(url)

# connection = engine.connect()

# with engine.connect() as conn:


# create delarative table with for user created database?
# create reflective database for imported table

from model import *

def main():
    print("where have i been? [the app: by kylen cheung]")
    print("select user (or create one!)")
    user_id = select_user()

    print("options (plz pick 1)")
    print("1. view cities") # allows to view all cities, or view my certain traits (like date, population, etc)
    print("2. add cities") # add cities to database
    user_choice = input("enter a number!: ")

    if user_choice == "1":
        view_cities(user_id)

    if user_choice == "2":
        add_cities(user_id)

    # need class to store city objects
    # maybe use array of city objects or something like that

def add_cities(user):
    print("Adding City")

    print("Enter a city name (try to be exact)")

    # query database using SQLalchamey to find match
    # store information matched

if __name__=="__main__":
    main()