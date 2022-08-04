from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Configuration
from flask_security import RoleMixin, UserMixin
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Configuration)

menu = [
    {'name': 'Роллы', 'url': '/sushi'},
    {'name': 'Пиццы', 'url': '/pizza'},
    {'name': 'Салаты', 'url': '/salads'},
    {'name': 'Закуски', 'url': '/snacks'},
    {'name': 'Корзина', 'url': '/my_cart'}
]

db = SQLAlchemy(app)
migrate = Migrate(app, db)
