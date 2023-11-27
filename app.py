import json

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import requests

app = Flask(__name__)

token = "6892121869:AAEeEV8i4L1cQ5aF6KazqFjIDKDIZSUm4mg"
link = "https://api.telegram.org/bot" + token


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
    print(request.json)
    message = request.form['message']
    user = message['from']

    print(message)
    print(user)

    # send_message(user['id'], 'Hello dear')
    return {
        "status": "ok"
    }


def send_message(user_id, message):
    data = {
        "chatId": user_id,
        "text": message
    }

    response = requests.post(
        url=link + "/sendMessage",
        json=data
    )
    return response.json()
