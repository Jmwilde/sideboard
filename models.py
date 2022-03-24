from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import os
import re

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, config):
    app.config.from_object(config)
    db.app = app
    db.init_app(app)
    db.create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

"""
Customers can save their favorite items
1 customer can have many favorites
1 favorite item can be liked by many customers
Hence we have a many to many relation
"""
favorite_items_table = db.Table('favorites',
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True)
)

"""
Customers can view purchased items
1 customer can purchase many items
1 item can be purchased by many customers
Hence we have a many to many relation
"""
purchased_items_table = db.Table('purchased',
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True)
)

"""
1 customer can buy from many different merchants
1 merchant can sell to many different customers
"""

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

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
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
    merchant_id = Column(Integer, db.ForeignKey('merchants.id'), nullable=False)
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

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

class Customer(db.Model):
    __tablename__ = "customers"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    favorites = db.relationship("Item", secondary=favorite_items_table)
    purchases = db.relationship("Item", secondary=purchased_items_table)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.favorites = []
        self.purchases = []

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'favorites': self.favorites,
        'purchases': self.purchases}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

