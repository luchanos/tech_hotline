from hotline_db.orders import TechOrder
from app import app
from flask import render_template, request


@app.route("/ping")
def ping():
    return "Pong"


@app.route("/new_order")
def new_order():
    return "new_order"


@app.route("/show_order")
def show_order():
    order_data = dict(order_messages="TEST",
                      order_id=1,
                      order_sounds=123,
                      order_images=12,
                      order_videos=45,
                      created_dt=1312,
                      status=123
                      )
    return render_template("single_order.html", title="ORDER", order_data=order_data, order=order_data)
