from flask_login import UserMixin


db = "login2_db"

class User(UserMixin,db):
    pass