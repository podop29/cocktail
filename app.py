from flask import Flask, request, render_template, flash, redirect, session
import requests
from crypt import methods
from models import connect_db, db, User, Post, Likes
from forms import SearchDrinkForm, UserForm, AddCommentForm
from helpers import create_drink_list, create_drink, create_drink_list_by_ingredient, create_drink_showcase, create_empty_drink, create_comments

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

@app.route('/drink/<int:id>', methods=['GET','POST'])
def show_drink_details(id):
    """Details page that shows details on one specific drink by id"""
    form = AddCommentForm()
    if form.validate_on_submit():
        new_comment = Post(text=form.text.data, user_id = session["user_id"], drink_id = id )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(f"/drink/{id}")



    res = requests.get(f"{BASE_API_URL}lookup.php?i={id}")
    data = res.json()
    drink = create_drink(data)
    #Gets comments for post
    posts = Post.query.filter_by(drink_id = id).all()
    user_ids = [post.user_id for post in posts]
    comments = []
    idx = 0
    #Loops through each post in the query and makes a comment object with username and text
    for post in posts:
        user_id = user_ids[idx]
        user = User.query.get(user_ids[idx])
        username = (user.username)
        idx += 1
        comments.append(create_comments(user_id,username, post.text))

    

    return render_template('show-drink-details.html', drink = drink, comments = comments, form = form)



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


#Login and register users
@app.route('/login', methods=['GET','POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid Username/Passwords']
    
    return render_template('login.html', form = form)


@app.route('/register', methods=["GET", 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash("Succsess")
        return redirect('/')
    else:
        return render_template('register.html', form=form)       
    

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



#Likes and comments
@app.route('/drink/<int:drinkid>/like')
def add_like(drinkid):
    """Route for adding a like to the db"""
    if "user_id" not in session:
        return redirect('/login')
    new_like = Likes(user_id = session["user_id"], drink_id = drinkid)
    db.session.add(new_like)
    db.session.commit()
    return redirect(f'/{session["user_id"]}/likes')


@app.route('/<int:user_id>/likes')
def show_likes(user_id):
    """Route for showing a user their likes"""
    if "user_id" not in session:
        return redirect('/login')
    likes = Likes.query.filter_by(user_id = user_id)
    drink_list_ids = []
    drink_list = []

    for like in likes:
        id = like.drink_id
        drink_list_ids.append(id)
    
    idx = 0
    for drink in drink_list_ids:
        data = requests.get(f"{BASE_API_URL}lookup.php?i={drink_list_ids[idx]}").json()
        drink = create_drink(data)
        drink_list.append(drink)
        idx += 1


    return render_template('show-likes.html', drinks = drink_list)

@app.route('/<int:user_id>/likes/remove/<int:drink_id>', methods=["POST"])
def remove_drink(user_id,drink_id):
    likes = Likes.query.filter_by(drink_id = drink_id).first()
    db.session.delete(likes)
    db.session.commit()
    return redirect(f'/{user_id}/likes')

#Comments



