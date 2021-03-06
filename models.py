"""create model for users"""

from enum import unique
from optparse import Values
from flask_sqlalchemy import SQLAlchemy
import datetime 

# Not understanding the use of the above imports completely. 

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"


    @classmethod
    def __repr__(self):
        u = self
        return f"<User id={u.id} name={u.first_name} species={u.last_name} hunger={u.img_url}>"
        
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(25), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    img_url = db.Column(db.String, nullable=True)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    @classmethod
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default= datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class PostTag(db.Model):
    """Post and Tag connected"""

    __tablename__ = "posts_tags"

    @classmethod
    def __repr__(self):
        pt = self
        return f"<PostTag post_id={pt.post_id} tag_id={pt.tag_id}>"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True, nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)

class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    @classmethod
    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', cascade="all,delete", backref='tags')







