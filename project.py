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

import sys

def main():

    print("where have i been? [the app: by kylen cheung]")
    print("select user (or create one!)")

    user_id = select_user()

    user_choice = 4
    while(user_choice != 3):

        print("options (plz pick 1)")
        print("1. view cities") # allows to view all cities, or view my certain traits (like date, population, etc)
        print("2. add cities") # add cities to database
        print("3. exit program")
        user_choice = int(input("enter a number!: "))

        if user_choice == 1:
            view_cities(user_id)

        if user_choice == 2:
            add_cities(user_id)

        if user_choice == 3:
            sys.exit()

    # need class to store city objects

    # maybe use array of city objects or something like that


if __name__=="__main__":
    main()