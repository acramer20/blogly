"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "chickenzarecool1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Redirects to users page"""
    return redirect("/users")

@app.route('/users')
def list_users():
    """shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users = users)

# @app.route('/users/add_user', methods=['GET'])
# def add_user_form():
#     """going to the form to add new user"""

#     return render_template('add_user.html')

@app.route('/users/add_user', methods=['GET', 'POST'])
def add_user():
    """Using form to create new user"""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        img_url = request.form['img_url']

        new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')

    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows the user's details"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

# @app.route('/users/<int:user_id>/edit')
# def show_user(user_id):
#     """Shows edit form"""
#     user = User.query.get_or_404(user_id)
#     return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def users_edit(user_id):
    """Editing the existing user's info"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.img_url = request.form['img_url']

        db.session.add(user)
        db.session.commit()
    
        return redirect('/users')

    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

