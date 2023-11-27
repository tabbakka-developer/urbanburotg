from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)

token = "6945010116:AAFNH2do-0VR_WPFoG6HgEzMC_pnWd2FOR0"
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



@app.route("/api/tg-webhook", methods=['POST'])
def tg_init():
    return
