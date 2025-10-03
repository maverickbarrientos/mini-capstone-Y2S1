from flask import Flask, render_template, session
from flask_cors import CORS
from routes.admin_route import admin_route

app = Flask(__name__)
app.register_blueprint(admin_route, url_prefix="/admin") 
CORS(app)

app.config["SECRET_KEY"] = "iloveyou123"

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)