"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
michael = User(first_name='Michael', last_name='Scott', img_url='https://en.wikipedia.org/wiki/Michael_Scott_(The_Office)#/media/File:MichaelScott.png')
wendy = User(first_name='Wendy', last_name='Byrde', img_url='https://ozark-netflix.fandom.com/wiki/Wendy_Byrde?file=Wendy.png')
britney = User(first_name='Britney', last_name='Spears', img_url='https://en.wikipedia.org/wiki/Britney_Spears#/media/File:Britney_Spears_2013_(Straighten_Crop).jpg')

# Add new objects to session, so they'll persist
db.session.add(michael)
db.session.add(wendy)
db.session.add(britney)

# Commit--otherwise, this never gets saved!
db.session.commit()