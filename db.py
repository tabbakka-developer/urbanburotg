import sqlite3


class DB:

    def __int__(self):
        self.connection = sqlite3.connect('urbanburo_database.db')
        self.cursor = self.connection.cursor()
        self.init_users_table()

    def init_users_table(self):
        self.cursor.execute('''
        CREATE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY
        telegram_id BIGINT
        first_name VARCHAR(255) DEFAULT NULL
        last_name VARCHAR(255) DEFAULT NULL
        username VARCHAR(255) DEFAULT NULL
        ''')
        self.connection.commit()

    def set_user(self, telegram_id, first_name = None, last_name = None, username = None):
        self.cursor.execute(
            'INSERT INTO Users (telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?)',
            (telegram_id, first_name, last_name, username)
        )
        self.connection.commit()

    def get_user_by_telegram_id(self, telegram_id):
        self.cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id))
        return self.cursor.fetchall()
