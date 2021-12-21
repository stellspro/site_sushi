from app import app, menu, db
from flask import render_template, url_for, request, redirect, session, flash
from models import Product, Category, Cart, Order
import json

list_empty = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Магазин "Sushi Max"', menu=menu)


@app.route('/pizza', methods=['POST', 'GET'])
def show_pizza():
    # if 'products' not in session:
    #     session['products'] = list_empty[:]
    # if request.method == 'POST':
    #     list_product = session['products']
    #     list_product.append(int(request.form['index']))
    #     session['products'] = list_product
    #     print(list_product)
    #     # session['products'] = int(request.form['index'])
    #     category = Category.query.filter(Category.id == 1).first()
    #     pizzas = category.Products.all()
    #     return render_template('pizza.html', title='Наши пиццы', pizzas=pizzas, menu=menu)
    # category = Category.query.filter(Category.id == 1).first()
    # pizzas = category.Products.all()

    return render_template('pizza.html', title='Наши пиццы', menu=menu)


@app.route('/get-pizza', methods=['POST', 'GET'])
def get_pizza():
    products = {}
    category = Category.query.filter(Category.id == 1).first()
    pizzas = category.Products.all()
    for i in pizzas:
        b = {'id': f'{i.id}', 'name': f'{i.name}', 'description': f'{i.description}', 'price': f'{int(i.price)}',
             'image': f'{i.image}'}
        products[i.id] = b
    json_products = json.dumps(products)
    return json_products


@app.route('/my_cart', methods=['POST', 'GET'])
def my_cart():
    if request.method == 'POST':
        render_template('index.html', menu=menu)
    return render_template('my_cart.html', title='Корзина', menu=menu)


@app.route('/get-products', methods=['GET', 'POST'])
def get_products():
    products = {}
    list_products = Product.query.all()
    for i in list_products:
        b = {'id': f'{i.id}', 'name': f'{i.name}', 'description': f'{i.description}', 'price': f'{int(i.price)}'}
        products[i.id] = b
    json_products = json.dumps(products)
    return json_products


@app.route('/order_page', methods=['POST', 'GET'])
def checkout():
    name = request.json['user_name']
    phone = request.json['phone']
    address = request.json['address']
    payment = request.json['payment']
    products_id = request.json['id']
    products_coast = request.json['coast']
    order = Order(user_name=name, phone=phone, address=address, payment=payment)
    db.session.add(order)
    db.session.commit()
    print(products_id, products_coast)
    for i in range(len(products_id)):
        cart = Cart(order_id=order.id, product_id=products_id[i], count=products_coast[i])
        db.session.add(cart)
        db.session.commit()
        print('Успешно')
    return render_template('index.html')

    # try:
    #     db.session.add(order)
    #     db.session.commit()
    # except:
    #     print('something wrong')
    #     flash('Что то пошло не так', category='error')
    # try:
    #     for product in products_id:
    #         cart = Cart(order_id=order.id, product_id=int(product))
    #         db.session.add(cart)
    #         db.session.commit()
    #     flash('Заказ оформлен', category='success')
    # except:
    #     print('something wrong')
    #     flash('Что то пошло не так', category='error')
    # session['products'] = list_empty[:]
    # return render_template('my_cart.html', menu=menu, title='Корзина')
