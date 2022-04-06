"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

# routes for Posts

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post_form(user_id):
# NEED REMINDER AS TO WHERE WE ARE GETTING user_id FROM and why we put it there in the first place. 
    """form for adding a new post"""
    user = User.query.get_or_404(user_id)

    if request.method =='POST':
        new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user.id) 
        # **** may need to adjust the user_id somehow ***
        db.session.add(new_post)
        db.session.commit()
        # could add in a flash here

        return redirect(f"/users/{user_id}")

    return render_template('posts/new.html', user = user)

@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post_contents(post_id):
    """Show the contents of each user's posts"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/details.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def post_edit(post_id):
    """Editing the existing user's info"""
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.user_id = f"{post.user_id}"

        db.session.add(post)
        db.session.commit()
    
        return redirect(f'/users/{post.user_id}')

    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete an existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
    # Again here the use of user_id (explain) *******





