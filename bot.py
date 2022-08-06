import telebot
from telebot import types
from config import token
from models import Product, Category, Cart, Order
from app import db
from dataclasses import dataclass
from flask import session

bot = telebot.TeleBot(f'{token}')
sessions = {}
p_image = ['🍕', '🍣', '🥗', '🍤']


@dataclass
class ProductInCart:
    product_id: int
    product_coast: int

    def __repr__(self):
        return f'{self.product_id} {self.product_coast}'


@bot.message_handler(commands=['start'])
def start(message):
    """Обработка команды 'start'"""
    sessions[f'{message.chat.id}'] = {'products': {}}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_menu = types.KeyboardButton('🍽 Меню')
    btn_cart = types.KeyboardButton('🗑 Корзина')
    btn_news = types.KeyboardButton('📬 Новости')
    btn_about_us = types.KeyboardButton('📜 О нас')
    markup.add(btn_menu, btn_cart, btn_news, btn_about_us)
    bot.send_message(message.chat.id, '<strong>Добро пожаловать в наш магазин!</strong>', parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types='text')
def menu(message):
    if message:
        if message.text == '🍽 Меню':
            # обработка кнопки "Меню"
            markup = types.InlineKeyboardMarkup(row_width=2)
            print(type(markup))
            cat = Category.query.all()
            for i in range(len(cat)):
                category = Category.query.filter(Category.id == cat[i].id).first()
                btn = types.InlineKeyboardButton(f'{p_image[i]}   {cat[i]} ({len(category.Products.all())})',
                                                 callback_data=f'{cat[i]}')
                markup.add(btn)
            bot.send_message(message.chat.id, '<b>Выберите категорию:</b>', parse_mode='html', reply_markup=markup)

        if message.text == '🗑 Корзина':
            # обработка кнопки "Корзина"
            if len(sessions[f'{message.chat.id}']['products']) == 0:
                # если корзина пустая
                cart_markup = types.InlineKeyboardMarkup(row_width=2)
                btn = types.InlineKeyboardButton('⬅️  В каталог', callback_data='back')
                cart_markup.add(btn)
                bot.send_message(message.chat.id, '🙁  Ваша корзина пуста', reply_markup=cart_markup)
            else:
                # если в корзине есть продукты
                products = sessions[f'{message.chat.id}']['products']
                print(products)
                if len(products) > 0:
                    for name, value in products.items():
                        print(name, value)
                        print(value.product_id)
                        product = Product.query.filter(Product.id == value.product_id).first()
                        buttons = types.InlineKeyboardMarkup(row_width=4)
                        btn_del = types.InlineKeyboardButton('❌', callback_data=f'delete{str(value.product_id)}')
                        btn_down = types.InlineKeyboardButton('⬇️', callback_data=f'down{value.product_id}')
                        btn_product = types.InlineKeyboardButton(f'{value.product_coast}', callback_data='produuuuct')
                        btn_up = types.InlineKeyboardButton('⬆', callback_data=f'up{value.product_id}')
                        buttons.add(btn_del, btn_down, btn_product, btn_up)
                        bot.send_message(message.chat.id,
                                         f'У вас в корзине - {product.name}, стоимость {product.price}',
                                         reply_markup=buttons)
                    bot.send_message(message.chat.id, text='Что делаем?',
                                     reply_markup=get_two_buttons('Оформить заказ', 'sc', 'Очистить корзину', 'del'))

        if message.text == '📜 О нас':
            # обработка кнопки "О нас"
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_edit = types.InlineKeyboardButton('Редактировать', callback_data='edit_message')
            markup.add(btn_edit)
            bot.send_message(message.chat.id, text='Тестовое сообщение', reply_markup=markup)


def get_two_buttons(name_first_btn, callback_data1, name_second_btn, callback_data2):
    """Возвращает две InlineKeyboardButton"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_first = types.InlineKeyboardButton(f'{name_first_btn}', callback_data=f'{callback_data1}')
    btn_second = types.InlineKeyboardButton(f'{name_second_btn}', callback_data=f'{callback_data2}')
    markup.add(btn_first, btn_second)
    return markup


def delete_from_cart(call, product):
    """Удаляет продукт из корзины пользователя"""
    del sessions[f'{call.message.chat.id}']['products'][f'{product.product_id}']
    bot.answer_callback_query(callback_query_id=call.id, text='Удалено из корзины')
    print(sessions[f'{call.message.chat.id}'])


def get_product(call, product_cat):
    """Отобращает продукты в переданной категории"""
    print(call.data)
    category = Category.query.filter(Category.id == product_cat).first()
    product = category.Products.all()[0:1]

    for key in product:
        user_session = call.message.chat.id
        if str(call.message.chat.id) in sessions and 'products' in sessions[str(user_session)] and str(
                key.name) in sessions[str(user_session)]['products']:
            # Если продукт добавлен в корзину, кнопка "Добавить в корзину" заменяется на "Удалить из корзины"
            pic = open(f'static/img/{key.image}', 'rb')
            bot.send_message(call.message.chat.id, key.name)
            bot.send_photo(call.message.chat.id, pic,
                           reply_markup=get_two_buttons('❌ Удалить из корзины',
                                                        f'delete{key.id}',
                                                        '⬅️ Назад',
                                                        'back'))

        else:
            # Если продукт не добавлен в корзину
            pic = open(f'static/img/{key.image}', 'rb')
            bot.send_message(call.message.chat.id, key.name)
            bot.send_photo(call.message.chat.id, pic, reply_markup=get_two_buttons('🛍 В корзину',
                                                                                   key.id,
                                                                                   '⬅️ Назад',
                                                                                   'back'))


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        products = [str(name.id) for name in Product.query.all()]
        print(products)
        # Обработка кнопки "пицца"
        if call.data == 'Пицца':
            category = Category.query.filter(Category.id == 1).first()
            pizzas = category.Products.all()[0:3]
            # btn = types.InlineKeyboardButton(str(key.name), callback_data=f'{key.id}')
            # markup.add(btn)
            bot.send_message(call.message.chat.id, '<b>Выберите пиццу:</b>', parse_mode='html')
            get_product(call, 1)

        if call.data == 'Роллы':
            # Обработка кнопки "роллы"
            bot.send_message(call.message.chat.id, '<b>Выберите ролл:</b>', parse_mode='html')
            get_product(call, 4)

        if call.data == 'Салаты':
            # Обработка кнопки "салаты"
            bot.send_message(call.message.chat.id, '<b>Выберите салат:</b>', parse_mode='html')
            get_product(call, 3)

        if call.data == 'Закуски':
            # Обработка кнопки "закуски"
            bot.send_message(call.message.chat.id, '<b>Выберите закуски:</b>', parse_mode='html')
            get_product(call, 2)

        if call.data == 'back':
            # Обработка кнопки "Назад"
            markup = types.InlineKeyboardMarkup(row_width=2)
            cat = Category.query.all()
            for i in range(len(cat)):
                category = Category.query.filter(Category.id == cat[i].id).first()
                btn = types.InlineKeyboardButton(f'{p_image[i]}  {cat[i]} ({len(category.Products.all())})',
                                                 callback_data=f'{cat[i]}')
                markup.add(btn)
            bot.send_message(call.message.chat.id, '<b>Выберите категорию:</b>', parse_mode='html', reply_markup=markup)

        if call.data in products:
            # Добавление продукта в корзину
            try:
                appended_product_id = (Product.query.filter(Product.id == call.data).first())
                print(type(appended_product_id.id), appended_product_id.id)
                appended_product = ProductInCart(product_id=appended_product_id.id, product_coast=1)
                sessions[f'{call.message.chat.id}']['products'][f'{appended_product.product_id}'] = appended_product
                print(sessions[f'{call.message.chat.id}']['products'])
                bot.answer_callback_query(callback_query_id=call.id, text='Добавлено в корзину')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=get_two_buttons('❌ Удалить из корзины',
                                                                           f'delete{appended_product.product_id}',
                                                                           '⬅️ Назад',
                                                                           'back'))
            except KeyError:
                print('ЧТо то пошло не так')
                print(sessions)

        if call.data == 'del':
            # Обработка кнопки "Очистить корзину"
            sessions[f'{call.message.chat.id}']['products'].clear()
            cart_markup = types.InlineKeyboardMarkup(row_width=2)
            btn = types.InlineKeyboardButton('🥢 В каталог', callback_data='back')
            cart_markup.add(btn)
            bot.send_message(call.message.chat.id, '🙁 Корзина пуста', reply_markup=cart_markup)

        if call.data == 'sc':
            # Обработка кнопки "Оформить заказ"
            name = 'denis'
            phone = '1234'
            address = '30 let WLKSM'
            payment = 'наличные'
            pr = [product_id for product_id in sessions[f'{call.message.chat.id}']['product_id']]
            products_id = [Product.query.filter(Product.name == pr[i]).first().id for i in range(len(pr))]
            products_coast = 1
            order = Order(user_name=name, phone=phone, address=address, payment=payment)
            db.session.add(order)
            db.session.commit()
            for i in range(len(products_id)):
                cart = Cart(order_id=order.id, product_id=products_id[i], count=products_coast)
                db.session.add(cart)
                db.session.commit()
                print('Успешно')
            bot.send_message(call.message.chat.id, 'Успешно, ждите звонка оператора')

        if call.data.startswith('down'):
            # обработка кнопки "вниз"
            pr_id = int(call.data[4:])
            print(pr_id)
            pr = sessions[f'{call.message.chat.id}']['products'][f'{pr_id}']
            if pr.product_coast > 0:
                pr.product_coast -= 1
                buttons = types.InlineKeyboardMarkup(row_width=4)
                btn_del = types.InlineKeyboardButton('❌', callback_data=f'deleasdfteasdafa')
                btn_down = types.InlineKeyboardButton('⬇️', callback_data=f'down{pr_id}')
                btn_product = types.InlineKeyboardButton(
                    pr.product_coast,
                    callback_data='produuuuct')
                btn_up = types.InlineKeyboardButton('⬆', callback_data=f'up{pr_id}')
                buttons.add(btn_del, btn_down, btn_product, btn_up)
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=buttons)
            else:
                pass

        if call.data.startswith('up'):
            # обработка кнопки "вверх"
            print(call.data)
            pr_id = int(call.data[2:])
            print(pr_id)
            pr = sessions[f'{call.message.chat.id}']['products'][f'{pr_id}']
            print(pr)
            pr.product_coast += 1
            print(pr.product_coast)
            buttons = types.InlineKeyboardMarkup(row_width=4)
            btn_del = types.InlineKeyboardButton('❌', callback_data=f'deleasdfteasdafa')
            btn_down = types.InlineKeyboardButton('⬇️',
                                                  callback_data=f'down{pr.product_id}')
            btn_product = types.InlineKeyboardButton(
                pr.product_coast, callback_data='produuuuct')
            btn_up = types.InlineKeyboardButton('⬆', callback_data=f'up{pr.product_id}')
            buttons.add(btn_del, btn_down, btn_product, btn_up)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=buttons)

        if call.data.startswith('delete'):
            # Обработка кнопки "Удалить товар из корзины ❌"
            print(call.data)
            pr_id = int(call.data[6:])
            product = ProductInCart(product_id=pr_id, product_coast=1)
            delete_from_cart(call, product)

            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=get_two_buttons('🛍 Добавить в корзину',
                                                                       pr_id,
                                                                       '⬅️ Назад',
                                                                       'back'))


if __name__ == '__main__':
    print('Бот запущен')
    bot.infinity_polling()
