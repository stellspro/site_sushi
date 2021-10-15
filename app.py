from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stells:M0077dm111777@localhost/sushimaxshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'sat'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
menu = [{'name': 'Главная страница', 'url': '/'},
        {'name': 'Роллы', 'url': '/sushi'},
        {'name': 'Пиццы', 'url': '/pizza'},
        {'name': 'Салаты и закуски', 'url': '/salads'}
        ]

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500), nullable=True)
    active = db.Column(db.Boolean())
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<users {self.id}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))

    def __repr__(self):
        return f"<profiles {self.id}>"


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db.session.commit()


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Products, db.session))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Магазин "Sushi Max"', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
