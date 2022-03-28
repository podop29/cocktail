from flask import Flask, request, render_template, flash, redirect
import requests
from models import connect_db, db
from forms import SearchDrinkForm
from healpers import create_drink_list, create_drink

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "OOooOOOoOOOoo000"

#api variables
API_KEY = '9973533'
BASE_API_URL = f'https://www.thecocktaildb.com/api/json/v2/{API_KEY}/'


connect_db(app)

@app.route('/')
def show_home():
    res = requests.get(f"{BASE_API_URL}popular.php")
    random_data = requests.get(f"{BASE_API_URL}randomselection.php").json()
    data = res.json()
    drink_list = create_drink_list(data)
    random_drink_list = create_drink_list(random_data)
    return render_template("home.html", drinks = drink_list, random_drinks = random_drink_list )

@app.route('/drinks/<int:id>')
def show_drink_details(id):
    res = requests.get(f"{BASE_API_URL}lookup.php?i={id}")
    data = res.json()
    drink = create_drink(data)
    return render_template('show-drink-details.html', drink = drink)
