from flask import Flask, request, render_template, url_for, redirect
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_security import SQLAlchemyUserDatastore, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)

menu = [{'name': 'Главная страница', 'url': '/'},
        {'name': 'Роллы', 'url': '/sushi'},
        {'name': 'Пиццы', 'url': '/pizza'},
        {'name': 'Салаты и закуски', 'url': '/salads'},
        {'name': 'Корзина', 'url': '/my_cart'}
        ]

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://stells:M0077dm111777@localhost/sushimaxshop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

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


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


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


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Category, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(AdminView(Cart, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Магазин "Sushi Max"', menu=menu)


@app.route('/pizza')
def show_pizza():
    category = Category.query.filter(Category.id == 1).first()
    pizzas = category.Products.all()
    return render_template('pizza.html', title='Наши пиццы', pizzas=pizzas, menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
