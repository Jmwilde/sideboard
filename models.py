from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
import re

#TODO: Move session handling into a Base class that each Model inherits from

# Heroku / SQLAlchemy compatibility fix
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

print(f'DATABASE_URL:{uri}')

database_path = uri

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db_drop_and_create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Merchant
Contains contact info and a list of items
'''
class Merchant(db.Model):
    __tablename__ = 'merchants'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    email = Column(String(120))
    fb_link = Column(String(120))
    insta_link = Column(String(120))
    image_link = Column(String(500))
    description = Column(String(500))
    items = db.relationship("Item", backref="merchant", lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, city=None, state=None, phone=None, email=None,
                 fb_link=None, insta_link=None, image_link=None, description=None):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.email = email
        self.fb_link = fb_link
        self.insta_link = insta_link
        self.image_link = image_link
        self.description = description
        self.items = []

    def format(self):
        items_json = json.dumps([item.format() for item in self.items])
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'email': self.email,
            'fb_link': self.fb_link,
            'insta_link': self.insta_link,
            'image_link': self.image_link,
            'description': self.description,
            'items': items_json
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

class Item(db.Model):
    __tablename__ = "items"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500))
    image_link = Column(String(500))
    merchant_id = Column(Integer, db.ForeignKey('merchants.id'))
    # Item.merchant exists via backref

    def __init__(self, name, price, merchant_id, description=None, image_link=None):
        self.name = name
        self.price = price
        self.description = description
        self.image_link = image_link
        self.merchant_id = merchant_id

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'image_link': self.image_link,
        'merchant_id': self.merchant_id}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

class Customer(db.Model):
    __tablename__ = "customers"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(100), nullable=False)
    favorites = None
    purchases = None
    wishlist = None
