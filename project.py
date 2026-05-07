from model import *

import sys

def main():

    print("City Tracker")

    user_id = select_user()
    menu(user_id)

def menu(user_id):
    print("1. View Visited Cities") # allows to view all cities, or view my certain traits (like date, population, etc)
    print("2. Add City") # add cities to database
    print("3. Remove City")
    print("4. Exit Program")

    user_choice = 5
    while(user_choice != 4):
        user_choice = int(input("Choose an option: "))

        if user_choice == 1:
            view_cities(user_id)
            menu(user_id)
            return

        if user_choice == 2:
            add_cities(user_id)
            menu(user_id)
            return            

        if user_choice == 3:
            remove_cities(user_id)
            menu(user_id)
            return            
            
        if user_choice == 4:
            sys.exit()

if __name__=="__main__":
    main()