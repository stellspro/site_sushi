from models import User, Role, Product, Category, Order, Cart
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from app import app, db


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name="Home"))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Category, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(AdminView(Cart, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
