from flask import Flask, render_template, session
from mail_config import mail
from flask_cors import CORS
from routes.admin_route import admin_route
from routes.user_route import user_route
from routes.main import main
import dotenv
import os

app = Flask(__name__)

app.register_blueprint(admin_route, url_prefix="/admin")
app.register_blueprint(user_route, url_prefix="/user")
app.register_blueprint(main)
CORS(app)

app.config["SECRET_KEY"] = "iloveyou123"
app.config["UPLOAD_FOLDER"] = "static/plant_images/"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False

mail.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
#webhook