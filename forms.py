from flask_wtf import FlaskForm
from wtforms import StringField,RadioField, PasswordField
from wtforms.validators import InputRequired

class SearchDrinkForm(FlaskForm):
    'For searching drink'

    name = StringField("", validators=[InputRequired(message="Cant be Null")])
    choice = RadioField("Search by Drink Name or Ingredient", choices=[('drinks','drinks'),('ingredients','ingredients')], default='drinks')

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])