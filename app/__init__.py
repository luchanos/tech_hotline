from envparse import env
from flask import Flask

FLASK_APP = env.str("FLASK_APP", default="tech_hotline.py")

app = Flask(__name__)

from app import routes

app.run()
