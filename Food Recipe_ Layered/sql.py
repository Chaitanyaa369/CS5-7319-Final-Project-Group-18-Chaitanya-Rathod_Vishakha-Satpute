
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Users  # Import your User model


def user_data():
    # Create an SQLAlchemy engine (replace 'your_database_url' with your actual database URL)
    engine = create_engine('postgresql://postgres:postgres1@localhost/flask_db')

    # Create a session 
    Session = sessionmaker(bind=engine)
    session = Session()

    # Execute a query to retrieve all users from the 'users' table
    users = session.query(Users).all()

    # Display user data
    for user in users:
        print(f"User ID: {user.id}, Username: {user.username}, First Name: {user.first_name}, Last Name: {user.first_name}, Email: {user.email}")

    # Close the session
    session.close()
    
    return users
