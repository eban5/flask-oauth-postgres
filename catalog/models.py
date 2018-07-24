from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from catalog import db
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(500))
    items = db.relationship('Item')

    @property
    def serialize(self):
        # Serializable format
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture
        }


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    # add the relationship with the User class
    user = db.relationship('User')
    # Authorization: add a user_id field to map an item to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        # Returns object data in JSON
        return {
            'id': self.id,
            'name': self.name,
        }



class Item(db.Model):
    __tablename__ = 'item'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    # add the relationship with the User class
    user = relationship('User')
    # Authorization: add a user_id field to map an item to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        # Returns object data in JSON
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }

