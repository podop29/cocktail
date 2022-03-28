from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class SearchDrinkForm(FlaskForm):
    'For searching drink'

    name = StringField("Snack Name", validators=[InputRequired(message="Cant be Null")])