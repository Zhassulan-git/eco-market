from flask import flash, redirect, render_template, request, url_for
from app import app
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import *
from app import engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_user
from app.login import UserLogin


Session = sessionmaker(bind=engine)

@app.route("/register", methods=["GET","POST"])
def register():
    
    form = RegistrationForm()

    if form.validate_on_submit():
        print("ere")
        hashed_password = generate_password_hash(form.password.data)
        user = User(id=None, user_name=form.user_name.data, email=form.email.data, password=hashed_password)

        session = Session()

        if user:
            session.add(user)
            session.commit()
            flash("You successfully registered", "success")
            return redirect(url_for('login'))
   
    return render_template("register.html", title = "Registration", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
     
    form = LoginForm()
    if form.validate_on_submit():
        s = Session()
    
        user = s.query(User).filter(User.email==form.email.data).first()
        print(form.password.data)
        print(user.password)

        if user and check_password_hash(user.password, form.password.data):
            userlogin = UserLogin().create(user)
            login_user(userlogin)#set in app sessions info about user
            print("Session User created!")
            return redirect(url_for('index'))
        flash("Incorrect email or password")
    return render_template("login.html", title = "Registration", form=form)


#get user from db
def get_user(user_id):
    with Session() as s:
        user = s.query(User).filter_by(user_id = User.id).first()
        if not user:
            print("User is not exist")
            return False
        return user
