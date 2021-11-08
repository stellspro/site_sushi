from app import app, menu
from flask import render_template, url_for, request, redirect, session
from models import Product, Category


list_product = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Магазин "Sushi Max"', menu=menu)


@app.route('/pizza', methods=['POST', 'GET'])
def show_pizza():
    if request.method == 'POST':
        list_product.append(int(request.form['index']))
        session['products'] = list_product
        print(list_product)
        # session['products'] = int(request.form['index'])
        category = Category.query.filter(Category.id == 1).first()
        pizzas = category.Products.all()
        return render_template('pizza.html', title='Наши пиццы', pizzas=pizzas, menu=menu)
    category = Category.query.filter(Category.id == 1).first()
    pizzas = category.Products.all()
    return render_template('pizza.html', title='Наши пиццы', pizzas=pizzas, menu=menu)


@app.route('/my_cart', methods=['POST', 'GET'])
def my_cart():
    if request.method == 'POST':
        delete_product = int(request.form['delete_product'])
        list_product.remove(delete_product)
        session['products'] = list_product
        print(list_product)
        products_id = (session.get('products', []))
        products = Product.query.filter(Product.id.in_(products_id)).all()
        return render_template('my_cart.html', title='Корзина', menu=menu, products=products)
    products_id = (session.get('products', []))
    products = Product.query.filter(Product.id.in_(products_id)).all()
    return render_template('my_cart.html', title='Корзина', menu=menu, products=products)
