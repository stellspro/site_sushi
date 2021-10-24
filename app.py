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
        {'name': 'Салаты и закуски', 'url': '/salads'}
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
    category = db.relationship('Category', secondary=product_category,
                               backref=db.backref('Products', lazy='dynamic'))


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


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Category, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Магазин "Sushi Max"', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
