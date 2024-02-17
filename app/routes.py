import json
from flask import Response, jsonify, request
from app import app, engine
from app.models import *
from sqlalchemy.orm import sessionmaker

from base64 import b64encode

Session = sessionmaker(bind=engine)

@app.route('/', methods = ['GET'])
def index():
    session = Session()
    categories = session.query(Category).all()
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
    session = Session()
    foods = session.query(Food).all()
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
    session = Session()
    food_item = session.query(Food).get(food_id)
    serialized = [{
        'id' : food_item.id,
        'category_id': food_item.category_id,
        'title': food_item.title,
        'description':food_item.description,
        'image': food_item.image.decode('utf-8')}]
    
    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')

@app.route('/food/category/<string:category>', methods=['GET'])
def get_food_by_category(category):
    session = Session()
    categories = session.query(Category).all()
    for cat in categories:
        if cat.slug_string == category:
            cat_id = cat.id

    try:
        foods = session.query(Food).filter(Food.category_id==cat_id).all()

    except:
        return "No such data"
    serialized = []
    for f in foods:
        serialized.append({
            'id' : f.id,
            'category_id': f.category_id,
            'title': f.title,
            'price':f.price,
            'image': f.image.decode('utf-8')})
    
    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    session = Session()

    data = request.get_json()


    basket_Item = Basket(None,quantity=data['quantity'], food_id=data['id'])
    #this statement didn't work without insertion None for 'id' column
    session.add(basket_Item)
    session.flush()
    session.commit()

    serialized = [{
        'id':data['id'],
        'title': data['title'],
        'quantity': data['quantity'],
    }]

    json_data = json.dumps(serialized, ensure_ascii=False)

    return Response(json_data, content_type='application/json; charset=utf-8')

@app.route('/basket', methods=['GET'])
def basket():
    session = Session()
    #cart = Basket.query.all()
    cart = session.query(Basket, Food).join(Food, Food.id == Basket.food_id).all()
    data =[]
    for q,food_info in cart:
        print(type(food_info.image))
        image = food_info.image.decode('utf-8')
        data.append({
            'id': food_info.id, 
            'quantity': q.quantity, 
            'title': food_info.title, 
            'image': image,
            'price':food_info.price
        })
    
    json_data = json.dumps({'basket':data}, ensure_ascii=False)
    return Response(json_data, content_type='application/json; charset=utf-8')

