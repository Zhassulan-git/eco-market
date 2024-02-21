from datetime import datetime
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, LargeBinary , SmallInteger, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    id = Column("id",Integer, primary_key=True)
    title = Column("title",String, unique=True, nullable=False)
    image = Column("image",LargeBinary)
    slug_string = Column("slug_string",String(255), nullable = False)

    def __init__(self, id, title, image, slug_string):
        self.id = id
        self.title = title
        self.image = image
        self.slug_string = slug_string

    def __repr__(self):
        return f"({self.id} {self.title} {self.image} {self.slug_string})"

class Food(Base):
    __tablename__ = "food"
    id= Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image = Column(LargeBinary, nullable = True)
    price = Column(Integer, nullable = False)
    description = Column(String, nullable = True)
    slug_string = Column("slug_string",String(255), nullable = False)
    category_id = Column("category_id", Integer, ForeignKey('category_id'))

    def __init__(self, id, title, image, price, description, slug_string):
        self.id = id
        self.title = title
        self.image = image
        self.price = price
        self.description = description
        self.slug_string = slug_string
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"({self.id} {self.title} {self.image} {self.description} {self.price} {self.slug_string})"
    
    
class Basket(Base):
    __tablename__ = "basket"
    id= Column(SmallInteger, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable = False)
    food_id = Column(Integer, ForeignKey('food.id'), nullable = False)
    owner_id = Column("owner_id",Integer, ForeignKey('User.id'), nullable=False)

    
    def __init__(self, id,quantity, food_id):
        self.id = id
        self.quantity = quantity
        self.food_id = food_id
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"({self.id} {self.quantity} {self.food_id})"
    

class User(Base):
    __tablename__ = "users"
    id= Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column("user_name", String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, id,user_name, email, password):
        self.id=id
        self.user_name = user_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"({self.id} {self.email})"  


    

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key = True)
    order_date = Column(DateTime,
        default=func.now())
    total_amount = Column(Integer,nullable=False)
    number = Column("order_number",Integer, nullable=False)
    owner_id = Column("owner_id",Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, id, order_date,total_amount, number):
        self.id = id
        self.order_date = order_date
        self.total_amount = total_amount
        self.number = number

    def __repr__(self):
        return f"({self.id} {self.order_date} {self.total_amount} {self.number})"

class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key = True)
    quantity = Column(Integer, nullable = False)
    subtotal = Column(Integer,nullable=False)   
    delivery_cost = Column(Integer, nullable = True)
    food_id = Column(Integer, ForeignKey('food.id'))
    order_id = Column(Integer, ForeignKey('history.id'))

    
    def __init__(self, id, quantity, subtotal ,delivery_cost, food_id, order_id):
        self.id = id
        self.quantity = quantity
        self.subtotal = subtotal
        self.delivery_cost = delivery_cost
        self.food_id = food_id
        self.order_id = order_id

    def __repr__(self):
        return f"({self.id} {self.quantity} {self.subtotal} {self.delivery_cost} {self.food_id} {self.order_id})"
