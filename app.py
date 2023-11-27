import json

from flask import Flask
from flask import render_template
from flask import request
import requests
import sqlite3

app = Flask(__name__)

token = "6892121869:AAEeEV8i4L1cQ5aF6KazqFjIDKDIZSUm4mg"
link = "https://api.telegram.org/bot" + token
commandsList = [
    '/start',
    '/help',
    '/report'
]


@app.route("/")
def home():
    return "hello world"


@app.route("/admin", methods=['GET'])
def admin_main():
    return render_template('/admin/index.html')


@app.route("/api/qzwxecff123/set-hook", methods=['GET'])
def set_webhook():
    data = {
        "url": "https://vp-developer.pp.ua/api/tg-webhook"
    }
    response = requests.post(
        url=link + "/setWebhook",
        json=data
    )
    return response.json()


@app.route("/api/qzwxecff66613/getMe")
def get_me():
    response = requests.post(
        url=link + "/getMe"
    )
    return response.json()


@app.route("/api/tg-webhook", methods=['POST'])
def tg_init():
    # database
    init_users_table()

    json_data = request.get_json()
    message = json_data['message']
    text = message['text']
    user = message['from']
    store_user_if_needed(user)
    # for future
    chat = message['chat']
    parse_command(text, user['id'])
    return {
        "status": "ok"
    }


def send_message(user_id, message, keyboard=None):
    data = {
        "chat_id": user_id,
        "text": message
    }

    if keyboard is not None:
        data.reply_markup = keyboard

    response = requests.post(
        url=link + "/sendMessage",
        json=data
    )
    return response.json()


def store_user_if_needed(tg_user):
    users = get_user_by_telegram_id(telegram_id=tg_user['id'])
    print(users)
    if len(users) < 1:
        set_user(
            telegram_id=tg_user['id'],
            first_name=tg_user['first_name'],
            last_name=tg_user['last_name'],
            username=tg_user['username']
        )
        users = get_user_by_telegram_id(telegram_id=tg_user['id'])[0]
    return users[0]


def parse_command(command, user_id):
    print(command)
    if command in commandsList:
        if command == '/start':
            return command_start(user_id)
        elif command == '/help':
            return command_help(user_id)
        elif command == '/report':
            return command_report(user_id)
    else:
        return send_message(user_id, "Незнайома для мене команда. Вибач, я гарний але не ідеальний :(")


def command_start(user_id):
    return send_message(
        user_id,
        "Тут щось буде коли Давід скажи що тут має бути, адже зараз це просто текст",
        create_keyboard()
    )


def command_help(user_id):
    return send_message(user_id,
                        "Я вмію вітатись, та намагаюсь допомогти вам зробити наше місто кращим. Додаткова інформація тут зʼявіться пізниіше")


def command_report(user_id):
    return send_message(user_id, "Намагаюсь додати ваш репорт до нашої бази репортів")


def create_keyboard():
    return {
        'keyboard': [
            [
                {
                    'text': 'Відправити проблему',
                    'request_contact': 1,
                    'request_location': 1
                },
                {
                    'text': 'Соціальні мережі',
                },
            ],
            [
                {
                    'text': 'Правила поведінки'
                },
                {
                    'text': 'Мої скарги'
                }
            ]
        ],
        'is_persistent': 1
    }


#
#       DATABASE
#       Users table
#
def init_users_table():
    with sqlite3.connect('urbanburo_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            first_name TEXT DEFAULT NULL,
            last_name TEXT DEFAULT NULL,
            username TEXT DEFAULT NULL,
            is_admin INTEGER DEFAULT 0)
            ''')
        connection.commit()


def set_user(telegram_id, first_name=None, last_name=None, username=None):
    with sqlite3.connect('urbanburo_database.db') as connection:
        query = 'INSERT INTO Users (telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?)'
        values = (telegram_id, first_name, last_name, username)
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()


def get_user_by_telegram_id(telegram_id):
    with sqlite3.connect('urbanburo_database.db') as connection:
        query = 'SELECT * FROM Users WHERE telegram_id = ?'
        cursor = connection.cursor()
        cursor.execute(query, (telegram_id,))
        return cursor.fetchall()


#
#       Reports table
#
def init_reports_table():
    with sqlite3.connect('urbanburo_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reports (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            address TEXT NOT NULL,
            media TEXT DEFAULT NULL,
            FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE,
            is_draft INTEGER DEFAULT 1
            ''')
        connection.commit()


def set_new_report(user_id, message, address, media=None):
    with sqlite3.connect('urbanburo_database.db') as connection:
        query = 'INSERT INTO Reports (user_id, message, address, media) VALUES (?, ?, ?, ?)'
        values = (user_id, message, address, media)
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()


def make_active(report_id):
    with sqlite3.connect('urbanburo_database.db') as connection:
        query = 'UPDATE Reports SET is_draft = 0 WHERE id = ?'
        cursor = connection.cursor()
        cursor.execute(query, (report_id,))
        connection.commit()
