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
connection = sqlite3.connect('urbanburo_database.db')


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
    connection.close()
    return {
        "status": "ok"
    }


def send_message(user_id, message):
    data = {
        "chat_id": user_id,
        "text": message
    }

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
    return send_message(user_id, "Тут щось буде коли Давід скажи що тут має бути, адже зараз це просто текст")


def command_help(user_id):
    return send_message(user_id,
                        "Я вмію вітатись, та намагаюсь допомогти вам зробити наше місто кращим. Додаткова інформація тут зʼявіться пізниіше")


def command_report(user_id):
    return send_message(user_id, "Намагаюсь додати ваш репорт до нашої бази репортів")


#
# DATABASE
#
def init_users_table():
    connection.cursor().execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        first_name TEXT DEFAULT NULL,
        last_name TEXT DEFAULT NULL,
        username TEXT DEFAULT NULL)
        ''')
    connection.commit()


def set_user(telegram_id, first_name=None, last_name=None, username=None):
    query = 'INSERT INTO Users (telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?)'
    values = (telegram_id, first_name, last_name, username)

    with connection.cursor() as cursor:
        cursor.execute(query, values)

    connection.commit()


def get_user_by_telegram_id(telegram_id):
    query = 'SELECT * FROM Users WHERE telegram_id = ?'
    cursor = connection.cursor()
    cursor.execute(query, (telegram_id,))
    return cursor.fetchall()
