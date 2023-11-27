import json

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import requests

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
    json_data = request.get_json()
    message = json_data['message']
    text = message['text']
    user = message['from']
    # for future
    chat = message['chat']
    parse_command(text, user['id'])
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
    return send_message(user_id, "Я вмію вітатись, та намагаюсь допомогти вам зробити наше місто кращим. Додаткова інформація тут зʼявіться пізниіше")


def command_report(user_id):
    return send_message(user_id, "Намагаюсь додати ваш репорт до нашої бази репортів")
