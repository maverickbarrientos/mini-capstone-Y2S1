from flask import Flask, render_template
from flask_cors import CORS
from routes.admin_bp import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)