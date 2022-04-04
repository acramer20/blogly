"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


app.config['SECRET_KEY'] = "chickenzarecool1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
    """shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/add_user')
def add_user_form():
    """going to the form to add new user"""

    return render_template('/add_user.html')
@app.route('/', methods=['POST'])
def add_user():
    """Using form to create new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/', first_name=first_name, last_name=last_name, img_url=img_url)

# @app.route('/<int:pet_id>')
# def show_pet(pet_id):
#     """show details about a single pet"""
#     pet = Pet.query.get_or_404(pet_id) 
#     # This allows for you to respond with a 404 if it is not found. 
#     return render_template("details.html", pet=pet)

# @app.route("/species/<species_id>")
# def show_pets_by_species(species_id):
#     pets = Pet.get_by_species(species_id)
#     return render_template('species.html', pets=pets, species=species_id)
