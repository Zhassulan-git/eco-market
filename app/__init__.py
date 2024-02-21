from flask import Flask, Response, make_response
from sqlalchemy import create_engine, text
from flask_wtf import CSRFProtect

app = Flask(__name__)
db_url = 'postgresql://postgres:grespost@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'ebjrvnkjemebirb'
engine = create_engine(db_url, echo=True)
csrf = CSRFProtect(app)

from app import auth
from app import routes

# run for create tables if they arent exist
def create_db():

    with routes.Session() as session:
        with app.open_resource('site.db', mode='r') as f:
            session.execute(text(f.read()))
            session.commit()

            print("Tables for database successfully created!")


'''
function for generate csrf token then sending it from postman 
@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    Render a simple form with Flask-WTF to get the CSRF token
    You can use Flask's session to store the token temporarily
    from flask_wtf import FlaskForm
    from wtforms import StringField

    class MyForm(FlaskForm):
        name = StringField('Name')

    form = MyForm()
    csrf_token = form.csrf_token.current_token
    resp = make_response()
    resp.set_cookie('csrf_token', csrf_token)
    return resp
'''
