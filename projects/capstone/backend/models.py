
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json

load_dotenv()

database_path = os.environ["DATABASE_URL"]

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    

class Actor(db.Model):
    '''model for actors'''
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

class Movie (db.Model):
    '''model for movies'''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        EXAMPLE
            movie = Movie(title=movie_title, release_date=release_date)
            movie.insert()
    '''
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an existing model in database
        the model must exist in the database
        EXAMPLE
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
