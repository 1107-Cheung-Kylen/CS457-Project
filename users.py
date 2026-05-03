from sqlalchemy import select
from sqlalchemy import Column, String, Integer, REAL
from sqlalchemy.orm import declarative_base

from database import Session # avoid rewriting connection code from database.py

# sessionUsers = Session()

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'project'}

    name = Column(String)
    email = Column(String)
    id = Column(Integer, primary_key=True)

# new_user = Users(name = "Alice", email = "aliceg@unr.edu")

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