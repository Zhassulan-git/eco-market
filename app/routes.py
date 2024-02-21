import json
import random
from flask import Response, jsonify, request
from flask_login import LoginManager, login_user
from app import app, engine
from app.models import *
from sqlalchemy.orm import sessionmaker
from base64 import b64encode

Session = sessionmaker(bind=engine)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from app.login import UserLogin
    print("user_loaded")
    return UserLogin().fromDB(user_id)

@app.route('/', methods = ['GET'])
def index():
    session_cat = Session()
    categories = session_cat.query(Category).all()
    serialized = []
    for cat in categories:

        serialized.append({
            'id' :cat.id,
            'title': cat.title,
            'image': cat.image.decode('utf-8')
        })
    json_data = json.dumps(serialized, ensure_ascii=False)
    return Response(json_data, content_type='application/json; charset=utf-8')

#можно получить доступ к роуту и если у нас будет ендпоинт фуд мы не применяем фильтр а берем все товары 
#а если указана категория и ендпоинт фуд/категория то проводим фильтр по категории
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

#placing an order; add request data to history and order_details tables 
@app.route('/order_add', methods=['POST'])
def add_order():
    session = Session()
    data = request.get_json()
    #json format datas=> foods, quantity of each food, delivery cost
    cart = data.get('basket')
    delivery = data.get('delivery_cost')

    total_price = 0
    for food in cart:
        total_price += food['price'] 
    total_price+=delivery
    order_num = get_random_number()
    '''beacuse the sqlalcemy after 1.4 version doesnt't cache records
        I get the last record and +1 and will do it before create new query for history id and order_fk was equal 
    '''
    last_order = session.query(History).order_by(History.id.desc()).first()
    new_id = last_order.id + 1
    #add order to history
    order_item = History(id=new_id,order_date=None,total_amount=total_price,number = order_num)

    session.add(order_item)
    #add order to order_details
    for cart_item in cart:
        details_data = OrderDetails(id=None, 
                                    quantity=cart_item['quantity'], 
                                    subtotal=total_price-delivery, 
                                    delivery_cost=delivery,
                                    food_id=cart_item['id'],
                                    order_id=new_id
                                    )
        session.add(details_data)
    session.commit()

    return f"order created, id={order_num}"

def get_random_number():
    with Session as session:
        orders = session.query(History).all()
        numbers = []
        for num in orders:
            numbers.append(num)
        
        rand = random.randint(100000, 999999)
        while rand in numbers:
            rand = random.randint(100000, 999999)
    return rand 



@app.route('/search/', methods=['GET'])
def serach():
    session = Session()
    search_str = request.args.get('search_query')
    search_str.encode('utf-8')
    data = session.query(Food).filter(Food.title.ilike(f"%{search_str}%")).all()
    print(data)

    serialized = []
    for data_item in data:
        serialized.append({
            'id':data_item.id,
            'title':data_item.title,
            'price':data_item.price,
            'image':data_item.image.decode('utf-8')
        })

    json_data = json.dumps(serialized, ensure_ascii=False)
    return Response(json_data, content_type='application/json; charset=utf-8')
