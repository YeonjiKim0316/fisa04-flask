import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(__file__)

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

myDB = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
mySecret=os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = myDB
SQLALCHEMY_TRACK_MODIFICATIONS = False # 
SECRET_KEY=mySecret