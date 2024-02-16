import base64
import json

from flask import Response, request
from app.models import *
from app import app

@app.route('/', methods = ['GET'])
def index():
    categories = Category.query.all()
    serialized = []
    for cat in categories:

        serialized.append({
            'id' :cat.id,
            'title': cat.title,
            'image': cat.image.decode('utf-8')
        })
    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')
@app.route('/food', methods=['GET'])
def get_all_foods():
    foods = Food.query.all()
    serialized = []
    for f in foods:

        serialized.append({
            'id' : f.id,
            'category_id': f.category_id,
            'title': f.title,
            'image': f.image.decode('utf-8')
        })
    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')

@app.route('/food/<int:food_id>', methods=['GET'])
def get_food(food_id):

    food_item = Food.query.get(food_id)
    serialized = [{
        'id' : food_item.id,
        'category_id': food_item.category_id,
        'title': food_item.title,
        'description':food_item.description,
        'image': food_item.image.decode('utf-8')}]
    
    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    title = data['title']
    quantity = data['quantity']

    basket_Item = Basket(quantity=quantity, food_id=data['id'], )
    db.session.add(basket_Item)
    db.session.commit()

    serialized = [{
        'id':data['id'],
        'title':title,
        'quantity': quantity,
    }]

    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')



@app.route('/basket', methods=['GET'])
def basket():
    cart = Basket.query.all()
    serialized = []
    for cart_item in cart:

        serialized.append({
            'id' : cart_item.id,
            'food_id': cart_item.food_id
        })
    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')