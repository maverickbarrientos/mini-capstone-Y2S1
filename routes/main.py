from flask import Blueprint, flash, redirect, render_template, url_for, request, session
from models.auth import validate_login
from services.entity_services import newUser

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
    elif email == 'admin@gmail.com' and password == 'admin':
        return redirect(url_for('admin_route.admin_dashboard'))
    else:
        flash('You have entered an incorrect password! Please try again.', 'danger')
        return redirect(url_for('main.login'))
    
@main.route("/signup")
def signup():
    return render_template("signup.html")

@main.route("/signup_process", methods=["POST"])
def signup_process():
    new = newUser(request.form)
    new.insert_user()
    return redirect(url_for('main.signup'))