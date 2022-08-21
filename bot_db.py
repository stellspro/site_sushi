from models import Cart, Category, Order, Product
from redis_cart import get_the_whole_cart_user, get_product_in_cart
from app import db


def get_all_categories():
    """
    Получение всех категорий продуктов из БД
    :return: Список категорий
    """
    return Category.query.all()


def get_category_by_id(cat_id):
    """
    Получение категории продуктов из БД по id
    :param cat_id: id категории INT
    :return: Категория продукта
    """
    return Category.query.filter(Category.id == cat_id).first()


def get_count_products_in_category(category):
    """
    Получение количества продуктов категории из БД
    :param category: class Category
    :return: количество продуктов INT
    """
    return len(category.Products.all())


def get_all_products():
    """
    Получение всего списка продуктов из БД
    :return: список продуктов list
    """
    return [str(name.id) for name in Product.query.all()]


def get_product_by_id(product_id):
    """
    Получение продукта из БД по id
    :param product_id: id продукта INT
    :return: class Product
    """
    return Product.query.filter(Product.id == product_id).first()


def get_product_in_category(cat_id):
    """
    Получение продуктов из БД в переданной категории
    :param cat_id: id категории INT
    :return: Список продуктов
    """
    category = Category.query.filter(Category.id == cat_id).first()
    return category.Products.all()[0:1]


def ordering(call, name, phone, address, payment):
    """
    Сохранение данных заказа в БД
    :param call: callback chat telegram
    :param name: Имя пользователя
    :param phone: Телефон пользователя
    :param address: Адрес пользователя
    :param payment: Способ оплаты
    :return:
    """
    if get_the_whole_cart_user(f'order_user_id{call.message.chat.id}'):
        order = Order(user_name=name, phone=phone, address=address, payment=payment)
        db.session.add(order)
        db.session.commit()
        products_id = get_the_whole_cart_user(f'order_user_id{call.message.chat.id}')
        for i in products_id:
            cart = Cart(order_id=order.id, product_id=i,
                        count=int(get_product_in_cart(f'order_user_id{call.message.chat.id}', i)))
            print(cart)
            db.session.add(cart)
            db.session.commit()
            print('Успешно')
