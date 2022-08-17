import redis


class DataConn:
    """Подключение БД"""

    def __init__(self, host, port, password):
        self._host = host
        self._port = port
        self._password = password

    def __enter__(self):
        """
        Открыть соединение с БД
        """
        self.conn = redis.Redis(host=self._host, port=self._port, password=self._password)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрыть соединение с БД
        """
        self.conn.close()
        if exc_val:
            raise
