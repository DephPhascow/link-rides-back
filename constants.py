from dotenv import load_dotenv
from os import getenv

load_dotenv()

SECRET = getenv('SECRET')
SITE_HOST = getenv('SITE_HOST')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
DB_LOGIN = getenv('DB_LOGIN')
DB_PASSWORD = getenv('DB_PASSWORD')
REDIS_HOST = getenv('REDIS_HOST')