from flask import Blueprint, render_template

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin_dashboard")
def admin_dashboard():
    return render_template('index.html')

@admin_bp.route("/user_management")
def user_management():
    pass