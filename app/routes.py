import base64
from flask import jsonify
from app import Category
from app import app

@app.route('/')
def index():
    categories = Category.query.all()
    
    cat_data = [{'id': categories.id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify(cat_data)


@app.route('/basket')
def basket():
    return '<h1>Basket is empty</h1>'