from flask import Flask
#All Necessary Imports
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:grespost@localhost:5432/postgres'
db = SQLAlchemy(app)

from app import routes