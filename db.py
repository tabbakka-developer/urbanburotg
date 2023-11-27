import sqlite3


class DB:
    _connection = None
    _cursor = None

    def __int__(self):
        self._connection = sqlite3.connect('urbanburo_database.db')
        self._cursor = self._connection.cursor()
        self.init_users_table()

    def init_users_table(self):
        self._cursor.execute('''
        CREATE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY
        telegram_id BIGINT
        first_name VARCHAR(255) DEFAULT NULL
        last_name VARCHAR(255) DEFAULT NULL
        username VARCHAR(255) DEFAULT NULL
        ''')
        self._connection.commit()

    def set_user(self, telegram_id, first_name = None, last_name = None, username = None):
        self._cursor.execute(
            'INSERT INTO Users (telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?)',
            (telegram_id, first_name, last_name, username)
        )
        self._connection.commit()

    def get_user_by_telegram_id(self, telegram_id):
        self._cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id))
        return self._cursor.fetchall()
