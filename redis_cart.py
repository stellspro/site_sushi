from redis_con import DataConn
from config import psw_redis, port_redis, host_redis


def add_product_in_cart(user_id: str, product_id: str):
    """Добавление продукта в корзину"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.hset(name=user_id, key=product_id, value='1')
        redis_client.expire(user_id, 86400)


def get_the_whole_cart_user(user_id: str):
    """Отобразить названия всех товаров в корзине"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        return [int(key) for key in redis_client.hkeys(name=user_id)]


def get_product_in_cart(user_id: str, product_id: str):
    """Отобразить  колличество конкретных продуктов в корзине"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        return int(redis_client.hget(user_id, product_id))


def plus_product_in_cart(user_id: str, product_id: str):
    """Снизить количество конкретных продуктов на один"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        coast = int(redis_client.hget(user_id, product_id))
        coast += 1
        redis_client.hset(user_id, product_id, coast)
        redis_client.expire(user_id, 86400)


def minus_product_in_cart(user_id: str, product_id: str):
    """Снизить количество конкретных продуктов на один"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        coast = int(redis_client.hget(user_id, product_id))
        coast -= 1
        redis_client.hset(user_id, product_id, coast)
        redis_client.expire(user_id, 86400)


def delete_product_in_cart(user_id: str, product_id: str):
    """Удалить продукт из корзины"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.hdel(user_id, product_id, product_id)


def empty_the_cart(user_id: str):
    """Очистить корзину"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.delete(user_id)
