from redis_con import DataConn
from config import psw_redis, port_redis, host_redis


def save_name(message):
    """
    Сохранение имени пользователя
    :param message: callback message telegram
    """
    user_id = f'user_data-{message.chat.id}'
    user_name = message.text
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.hset(name=user_id, key='user_name', value=user_name)
        redis_client.expire(user_id, 86400)


def save_phone(message):
    """
    Сохранение телефона пользователя
    :param message: callback message telegram
    """
    user_id = f'user_data-{message.chat.id}'
    user_phone = message.text
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.hset(name=user_id, key='user_phone', value=user_phone)
        redis_client.expire(user_id, 86400)


def save_address(message):
    """
    Сохранение адреса пользователя
    :param message: callback message telegram
    """
    user_id = f'user_data-{message.chat.id}'
    user_address = message.text
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.hset(name=user_id, key='user_address', value=user_address)
        redis_client.expire(user_id, 86400)


def get_info_about_user(chat_id, info):
    """
    Получение данных о пользователе
    :param chat_id: id чата в телеграм
    :param info: тип запрашиваемой информации (имя, телефон, адрес)
    :return:
    """
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        return redis_client.hget(chat_id, info)
