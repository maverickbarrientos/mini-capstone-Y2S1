from flask import Blueprint, render_template, jsonify, request
from services.admin_services import newUser

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin_dashboard")
def admin_dashboard():
    return render_template('index.html')

@admin_bp.route("/user_management")
def user_management():
    return render_template("admin/user-management.html")

@admin_bp.route("/add_user", methods=["POST"])
def add_user():
    form = request.form.to_dict()
    new_user = newUser(form)
    insert = new_user.insert_user()
    return insert

@admin_bp.route("/damn_right")
def damn_right():
    return render_template("damn-right.html")