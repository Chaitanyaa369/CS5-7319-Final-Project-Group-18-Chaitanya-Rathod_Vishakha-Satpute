from models import Users, db
from app import login_manager, login_user

class UserService:
    def create_user(self, username, first_name, last_name, email, password):
        user = Users(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    def get_user_by_username(self, username):
        return Users.query.filter_by(username=username).first()

    def verify_password(self, user, password):
        return user.password == password

    def login_user(self, user):
        login_user(user)
