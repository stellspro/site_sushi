import telebot
from telebot import types
from config import token
from redis_cart import get_the_whole_cart_user, get_product_in_cart, add_product_in_cart, empty_the_cart,\
    delete_product_in_cart, plus_product_in_cart, minus_product_in_cart
from redis_user_data import save_name, save_phone, save_address, get_info_about_user
from bot_db import get_all_categories, get_product_in_category, get_category_by_id, get_count_products_in_category, \
    get_product_by_id, ordering, get_all_products

bot = telebot.TeleBot(f'{token}')
p_image = ['🍕', '🍣', '🥗', '🍤']


@bot.message_handler(commands=['start'])
def start(message):
    """Обработка команды 'start'"""
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
            # cat = Category.query.all()
            cat = get_all_categories()
            for i in range(len(cat)):
                # category = Category.query.filter(Category.id == cat[i].id).first()
                category = get_category_by_id(cat[i].id)
                btn = types.InlineKeyboardButton(
                    f'{p_image[i]}   {cat[i]} ({get_count_products_in_category(category)})',
                                                 callback_data=f'{cat[i]}'
                )
                markup.add(btn)
            bot.send_message(message.chat.id, '<b>Выберите категорию:</b>', parse_mode='html', reply_markup=markup)

        if message.text == '🗑 Корзина':
            # обработка кнопки "Корзина"
            if not get_the_whole_cart_user(f'order_user_id{message.chat.id}'):
                # если корзина пустая
                cart_markup = types.InlineKeyboardMarkup(row_width=2)
                btn = types.InlineKeyboardButton('⬅️  В каталог', callback_data='back')
                cart_markup.add(btn)
                bot.send_message(message.chat.id, '🙁  Ваша корзина пуста', reply_markup=cart_markup)
            else:
                # если в корзине есть продукты
                products = get_the_whole_cart_user(f'order_user_id{message.chat.id}')
                if len(products) > 0:
                    for product_id in products:
                        product_coast = get_product_in_cart(f'order_user_id{message.chat.id}', str(product_id))
                        product = get_product_by_id(product_id)
                        buttons = types.InlineKeyboardMarkup(row_width=4)
                        btn_del = types.InlineKeyboardButton('❌', callback_data=f'delete{str(product_id)}')
                        btn_down = types.InlineKeyboardButton('⬇️', callback_data=f'down{product_id}')
                        btn_product = types.InlineKeyboardButton(f'{product_coast}', callback_data='produuuuct')
                        btn_up = types.InlineKeyboardButton('⬆', callback_data=f'up{product_id}')
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


def show_product_in_category(call, cat_id):
    """Отобращает продукты в переданной категории"""
    product = get_product_in_category(cat_id)

    for key in product:
        user_session = call.message.chat.id
        cart = get_the_whole_cart_user(f'order_user_id{user_session}')
        if key.id in cart:
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


def get_two_buttons(name_first_btn, callback_data1, name_second_btn, callback_data2):
    """Возвращает две InlineKeyboardButton"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_first = types.InlineKeyboardButton(f'{name_first_btn}', callback_data=f'{callback_data1}')
    btn_second = types.InlineKeyboardButton(f'{name_second_btn}', callback_data=f'{callback_data2}')
    markup.add(btn_first, btn_second)
    return markup


def save_user_data(call, data, description, func):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if get_info_about_user(f'user_data-{call.message.chat.id}', data):
        btn_user_data = types.InlineKeyboardButton('Редактировать', callback_data=f'edit_{data}')
        markup.add(btn_user_data)
        user_data = get_info_about_user(f'user_data-{call.message.chat.id}', data).decode('utf-8')
        bot.send_message(call.message.chat.id, f"{description} {user_data}", reply_markup=markup)
    else:
        msg = bot.send_message(call.message.chat.id, f'Введите {description}')
        bot.register_next_step_handler(msg, func)


def edit_user_data(call, description, func):
    msg = bot.send_message(call.message.chat.id, f'Введите {description}')
    bot.register_next_step_handler(msg, func)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'user_name':
        save_user_data(call, 'user_name', 'Имя', save_name)

    if call.data == 'user_phone':
        save_user_data(call, 'user_phone', 'Телефон', save_phone)

    if call.data == 'user_address':
        save_user_data(call, 'user_address', 'Адрес', save_address)

    if call.data == 'edit_user_name':
        edit_user_data(call, 'Имя', save_name)

    if call.data == 'edit_user_phone':
        edit_user_data(call, 'Телефон', save_phone)

    if call.data == 'edit_user_address':
        edit_user_data(call, 'Адресс', save_address)
    if call.message:
        products = get_all_products()
        # Обработка кнопки "пицца"
        if call.data == 'Пицца':
            bot.send_message(call.message.chat.id, '<b>Выберите пиццу:</b>', parse_mode='html')
            show_product_in_category(call, 1)

        if call.data == 'Роллы':
            # Обработка кнопки "роллы"
            bot.send_message(call.message.chat.id, '<b>Выберите ролл:</b>', parse_mode='html')
            show_product_in_category(call, 4)

        if call.data == 'Салаты':
            # Обработка кнопки "салаты"
            bot.send_message(call.message.chat.id, '<b>Выберите салат:</b>', parse_mode='html')
            show_product_in_category(call, 3)

        if call.data == 'Закуски':
            # Обработка кнопки "закуски"
            bot.send_message(call.message.chat.id, '<b>Выберите закуски:</b>', parse_mode='html')
            show_product_in_category(call, 2)

        if call.data == 'back':
            # Обработка кнопки "Назад"
            markup = types.InlineKeyboardMarkup(row_width=2)
            cat = get_all_categories()
            for i in range(len(cat)):
                category = get_category_by_id(cat[i].id)
                btn = types.InlineKeyboardButton(
                    f'{p_image[i]}   {cat[i]} ({get_count_products_in_category(category)})',
                    callback_data=f'{cat[i]}'
                )
                markup.add(btn)
            bot.send_message(call.message.chat.id, '<b>Выберите категорию:</b>', parse_mode='html', reply_markup=markup)

        if call.data in products:
            # Добавление продукта в корзину
            try:
                appended_product_id = get_product_by_id(call.data)
                add_product_in_cart(f'order_user_id{call.message.chat.id}', appended_product_id.id)

                bot.answer_callback_query(callback_query_id=call.id, text='Добавлено в корзину')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=get_two_buttons('❌ Удалить из корзины',
                                                                           f'delete{appended_product_id.id}',
                                                                           '⬅️ Назад',
                                                                           'back'))
            except KeyError:
                bot.send_message(call.message.chat.id, 'Что то пошло не так')

        if call.data == 'del':
            # Обработка кнопки "Очистить корзину"
            cart_markup = types.InlineKeyboardMarkup(row_width=2)
            btn = types.InlineKeyboardButton('🥢 В каталог', callback_data='back')
            cart_markup.add(btn)
            empty_the_cart(f'order_user_id{call.message.chat.id}')
            bot.send_message(call.message.chat.id, '🙁 Корзина пуста', reply_markup=cart_markup)

        if call.data == 'sc':
            # Обработка кнопки "Оформить заказ"
            if get_info_about_user(f'user_data-{call.message.chat.id}', 'user_name') and \
                    get_info_about_user(f'user_data-{call.message.chat.id}', 'user_phone') and \
                    get_info_about_user(f'user_data-{call.message.chat.id}', 'user_address'):
                if get_the_whole_cart_user(f'order_user_id{call.message.chat.id}'):
                    ordering(call,
                             name=get_info_about_user(f'user_data-{call.message.chat.id}', 'user_name').decode('utf-8'),
                             phone=int(get_info_about_user(f'user_data-{call.message.chat.id}', 'user_phone')),
                             address=get_info_about_user(f'user_data-{call.message.chat.id}', 'user_address').decode(
                                 'utf-8'),
                             payment='наличные')
                else:
                    bot.send_message(call.message.chat.id, f'Добавьте что нибудь в корзину')
            else:
                bot.send_message(call.message.chat.id, f'Введите контактные данные')
                markup = types.InlineKeyboardMarkup(row_width=3)
                btn_user_name = types.InlineKeyboardButton('Имя', callback_data='user_name')
                btn_user_phone = types.InlineKeyboardButton('Телефон', callback_data='user_phone')
                btn_user_address = types.InlineKeyboardButton('Адрес', callback_data='user_address')
                btn_user_sc = types.InlineKeyboardButton('Оформить заказ', callback_data='sc')
                markup.add(btn_user_name, btn_user_phone, btn_user_address, btn_user_sc)
                bot.send_message(call.message.chat.id, text='Контактные данные', reply_markup=markup)

        if call.data.startswith('down'):
            # обработка кнопки "вниз"
            pr_id = int(call.data[4:])
            pr = get_product_in_cart(f'order_user_id{call.message.chat.id}', f'{pr_id}')
            if pr > 0:
                buttons = types.InlineKeyboardMarkup(row_width=4)
                btn_del = types.InlineKeyboardButton('❌', callback_data=f'deleasdfteasdafa')
                btn_down = types.InlineKeyboardButton('⬇️', callback_data=f'down{pr_id}')
                btn_product = types.InlineKeyboardButton(
                    get_product_in_cart(f'order_user_id{call.message.chat.id}', f'{pr_id}'),
                    callback_data='produuuuct')
                minus_product_in_cart(f'order_user_id{call.message.chat.id}', str(pr_id))
                btn_up = types.InlineKeyboardButton('⬆', callback_data=f'up{pr_id}')
                buttons.add(btn_del, btn_down, btn_product, btn_up)
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=buttons)
            else:
                pass

        if call.data.startswith('up'):
            # обработка кнопки "вверх"
            pr_id = int(call.data[2:])
            plus_product_in_cart(f'order_user_id{call.message.chat.id}', str(pr_id))
            buttons = types.InlineKeyboardMarkup(row_width=4)
            btn_del = types.InlineKeyboardButton('❌', callback_data=f'deleasdfteasdafa')
            btn_down = types.InlineKeyboardButton('⬇️',
                                                  callback_data=f'down{pr_id}')
            btn_product = types.InlineKeyboardButton(
                get_product_in_cart(f'order_user_id{call.message.chat.id}', f'{pr_id}'), callback_data='produuuuct')
            btn_up = types.InlineKeyboardButton('⬆', callback_data=f'up{pr_id}')
            buttons.add(btn_del, btn_down, btn_product, btn_up)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=buttons)

        if call.data.startswith('delete'):
            # Обработка кнопки "Удалить товар из корзины ❌"
            pr_id = int(call.data[6:])
            delete_product_in_cart(f'order_user_id{call.message.chat.id}', f'{pr_id}')

            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=get_two_buttons('🛍 Добавить в корзину',
                                                                       pr_id,
                                                                       '⬅️ Назад',
                                                                       'back'))


if __name__ == '__main__':
    print('Бот запущен')
    bot.infinity_polling()
