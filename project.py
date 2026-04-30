
def main():
    print("where have i been? [the app: by kylen cheung]")
    print("options (plz pick 1)")
    print("1. view cities") # allows to view all cities, or view my certain traits (like date, population, etc)
    print("2. add cities") # add cities to database
    user_choice = input("enter a number!: ")

    if user_choice == "1":
        view_cities()

    if user_choice == "2":
        add_cities()

    # need class to store city objects
    # maybe use array of city objects or something like that

def view_cities():
    print("Viewing Cities")
    
    # use SQLalchamey (do NOT load entire database into array)

def add_cities():
    print("Adding City")

    print("Enter a city name (try to be exact)")

    # query database using SQLalchamey to find match
    # store information matched


if __name__=="__main__":
    main()