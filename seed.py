from flask import session
from models import db, connect_db, User, Post
from app import app

db.drop_all()
db.create_all()

