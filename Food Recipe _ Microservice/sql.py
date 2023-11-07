
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Users 

def user_data():
    engine = create_engine('postgresql://postgres:postgres1@localhost/flask_db')

    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(Users).all()

    for user in users:
        print(f"User ID: {user.id}, Username: {user.username}, First Name: {user.first_name}, Last Name: {user.first_name}, Email: {user.email}")

    session.close()
    
    return users
