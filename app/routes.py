from app import app
from flask import request
from marshmallow import EXCLUDE

from schemas.orders import NewOrderSchema


@app.route("/ping")
def ping():
    return "Pong"


class Resources:
    """Класс для хранения всех необходимых приложению ресурсов."""
    pass


@app.route("/new_order", methods=["POST"])
def new_order():
    getted_data = request.get_json()
    # todo luchanos надо это потом засунуть в хэндлер
    schema = NewOrderSchema(unknown=EXCLUDE)
    res = schema.load(getted_data)
    return res
