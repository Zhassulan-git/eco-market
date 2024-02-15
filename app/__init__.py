from flask import Flask
#All Necessary Imports
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:grespost@localhost:5432/postgres'
db = SQLAlchemy(app)

from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.LargeBinary, unique=True)

class Food(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    image = db.Column(db.LargeBinary, nullable = True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('food', lazy=True))
    
class Basket(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable = False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable = False)
    food = db.relationship('Food',
        backref=db.backref('basket', lazy=True))
    

class History(db.Model):


    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    total_amount = db.Column(db.Integer,nullable=False)
    delivery_cost = db.Column(db.Integer, nullable = True)

class OrderDetails(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)
    subtotal = db.Column(db.Integer,nullable=False)

from app import routes