"""create model for users"""

from enum import unique
from optparse import Values
from flask_sqlalchemy import SQLAlchemy

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




