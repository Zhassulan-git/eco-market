import os 
from dotenv import load_dotenv # Режим отладки (уберите при переходе в production)

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False