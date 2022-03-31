from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    img_url = db.Column(db.Text, nullable=True)

    likes = db.relationship('Likes', backref="users")



    @classmethod
    def register(cls, username, password):
        'Register user with hashed password and return user'

        hashed = bcrypt.generate_password_hash(password)
        #turn byteststring into normal string
        hashed_utf8 = hashed.decode("utf8")

        #return instance of user annd hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls,username,pwd):
        "Validate that user exists and password is correct"

        u= User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

#----------------------------------------------------------------------#

class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    drink_id = db.Column(db.Integer)


    user = db.relationship('User', backref='posts')

#----------------------------------------------------------------------#


class Likes(db.Model):
    """Mapping user likes to drinks."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    drink_id = db.Column(
        db.Integer)
      
