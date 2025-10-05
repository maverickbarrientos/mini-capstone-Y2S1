from flask import Blueprint, redirect, render_template, url_for, request, session
from models.auth import validate_login

main = Blueprint("main", __name__)

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/login_process", methods=["POST", "GET"])
def login_process():
    email = request.form.get("email-input")
    password = request.form.get("password-input")
    login = validate_login(email, password)
    session["USER_LOGGED_IN"] = login
    if login is not None:
        return redirect(url_for('user_route.user_dashboard'))
    else:
        return redirect(url_for('main.login'))