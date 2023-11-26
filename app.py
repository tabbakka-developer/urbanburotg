from flask import Flask
from flask import render_template

app = Flask(__name__)

token = "6945010116:AAFNH2do-0VR_WPFoG6HgEzMC_pnWd2FOR0"
link = "https://api.telegram.org/bot" + token

@app.route("/")
def home():
    return "hello world"


@app.route("/admin", methods=['GET'])
def admin_main():
    return render_template('/admin/index.html')
