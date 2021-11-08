from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import joinedload
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

menu = [{'name': 'Главная страница', 'url': '/'},
        {'name': 'Роллы', 'url': '/sushi'},
        {'name': 'Пиццы', 'url': '/pizza'},
        {'name': 'Салаты и закуски', 'url': '/salads'},
        {'name': 'Корзина', 'url': '/my_cart'}
        ]

db = SQLAlchemy(app)
migrate = Migrate(app, db)



# def create_app():
#     """Application-factory pattern"""
#     ...
#     ...
#     db.init_app(app)
#     migrate.init_app(app, db)
#     ...
#     ...
#     return app

#
# order = Order.query.filter(Order.id == 1).first()
# # my_products = Cart.query.filter(Order.user_name == 'Петя')
# my = order.carts
#
# products = my.options(joinedload('product'))
#
# return render_template('my_cart.html', title='Корзина', menu=menu, products=products)



