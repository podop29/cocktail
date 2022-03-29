from flask import Flask, request, render_template, flash, redirect
import requests
from models import connect_db, db
from forms import SearchDrinkForm
from helpers import create_drink_list, create_drink, create_drink_list_by_ingredient, create_drink_showcase, create_empty_drink

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "OOooOOOoOOOoo000"

#api variables
API_KEY = '9973533'
BASE_API_URL = f'https://www.thecocktaildb.com/api/json/v2/{API_KEY}/'


connect_db(app)


@app.route('/', methods=["POST","GET"])
def show_home():
    """Home Page that shows random drinks, popular drinks, and a search form"""

    form = SearchDrinkForm()
    #If the form is filled out, will redirect to the search route
    if form.validate_on_submit():
        name = form.name.data
        choice = form.choice.data
        return redirect(f'/{choice}/{name}')
    #if the form isnt filled out, will show the home page
    data = requests.get(f"{BASE_API_URL}popular.php").json()
    random_data = requests.get(f"{BASE_API_URL}randomselection.php").json()
    drink_list = create_drink_showcase(data)
    random_drink_list = create_drink_showcase(random_data)
    return render_template("home.html", drinks = drink_list, random_drinks = random_drink_list, form=form )

@app.route('/drink/<int:id>')
def show_drink_details(id):
    """Details page that shows details on one specific drink by id"""
    res = requests.get(f"{BASE_API_URL}lookup.php?i={id}")
    data = res.json()
    drink = create_drink(data)
    return render_template('show-drink-details.html', drink = drink)



@app.route('/drinks/<name>')
def show_searched_drinks(name):
    """Shows all drinks that match the search"""
    data = requests.get(f"{BASE_API_URL}search.php?s={name}").json()
    try:
        drink_list = create_drink_list(data)
    except:
        #If the try fails, returns an drink that just says seearch not found
        drink_list = create_empty_drink()
    return render_template('show-searched-drinks.html', drinks = drink_list, name = name)

@app.route('/ingredients/<name>')
def show_searched_ingredients(name):
    """Shows all drinks that have the searched ingredient in them"""
    query = name.replace(" ", "%20")
    res = requests.get(f"{BASE_API_URL}filter.php?i={query}")
    data = res.json()
    try:
        drink_list = create_drink_list_by_ingredient(data)
    except:
        #If the try fails, returns an drink that just says seearch not found
        drink_list = create_empty_drink()
    return render_template('show-searched-drinks.html', drinks = drink_list, name = name)

        
    



