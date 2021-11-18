from app import app, menu, db
from flask import render_template, url_for, request, redirect, session
from models import Product, Category, Cart, Order

list_empty = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Магазин "Sushi Max"', menu=menu)


@app.route('/pizza', methods=['POST', 'GET'])
def show_pizza():
    if 'products' not in session:
        session['products'] = list_empty[:]
    if request.method == 'POST':
        list_product = session['products']
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
        if 'products' not in session:
            session['products'] = list_empty[:]
        else:
            list_product = session['products']
            delete_product = int(request.form['delete_product'])
            session['products'] = list_product
            list_product.remove(delete_product)
            print(list_product)
            products_id = (session.get('products', []))
            products = Product.query.filter(Product.id.in_(products_id)).all()
            return render_template('my_cart.html', title='Корзина', menu=menu, products=products)
    products_id = (session.get('products', []))
    products = Product.query.filter(Product.id.in_(products_id)).all()
    return render_template('my_cart.html', title='Корзина', menu=menu, products=products)


@app.route('/order_page', methods=['POST'])
def checkout():
    products_id = (session.get('products', []))
    name = request.form['first_name']
    phone = request.form['phone']
    address = request.form['address']
    order = Order(user_name=name, phone=phone, address=address, payment='наличными')
    try:
        db.session.add(order)
        db.session.commit()
    except:
        print('something wrong')
    for product in products_id:
        cart = Cart(order_id=order.id, product_id=int(product))
        try:
            db.session.add(cart)
            db.session.commit()
        except:
            print('something wrong')
    session['products'] = list_empty[:]
    return redirect(url_for('index'))
