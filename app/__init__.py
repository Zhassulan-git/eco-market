from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
db_url = 'postgresql://postgres:grespost@localhost:5432/postgres'
engine = create_engine(db_url, echo=True)

if __name__ == '__main__':
    app.run(debug=True)

from app import routes