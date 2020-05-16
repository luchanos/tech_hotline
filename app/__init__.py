from envparse import env
from flask import Flask

# todo luchanos понять зачем тут эта переменная и  проверить структуру самого этого файла
FLASK_APP = env.str("FLASK_APP", default="tech_hotline.py")

app = Flask(__name__)

from app import routes
