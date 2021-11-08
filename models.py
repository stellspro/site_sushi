from app import db
from flask_security import RoleMixin, UserMixin
from datetime import datetime


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

product_category = db.Table('product_category',
                            db.Column('product_id', db.Integer(), db.ForeignKey('product.id')),
                            db.Column('category_id', db.Integer(), db.ForeignKey('category.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    date = db.Column(db.DateTime, default=datetime.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer())
    discount_price = db.Column(db.Integer())
    image = db.Column(db.String(255))
    category = db.relationship('Category', secondary=product_category,
                               backref=db.backref('Products', lazy='dynamic'))

    carts = db.relationship('Cart', backref='product', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))

    def __repr__(self):
        return '{}'.format(self.name)


# Корзина + заказ
class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(80))
    phone = db.Column(db.Integer())
    address = db.Column(db.Text)
    payment = db.Column(db.String(15))
    date = db.Column(db.DateTime, default=datetime.now())
    carts = db.relationship('Cart', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'{self.user_name}, адрес: {self.address}, номер телефона: {self.phone}'


class Cart(db.Model):
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'), primary_key=True)
    count = db.Column(db.Integer())




