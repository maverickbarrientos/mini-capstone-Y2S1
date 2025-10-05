from flask import Blueprint, redirect, render_template, url_for, request, session
from models.user_models.greenhouse_model import get_default_plants

user_route = Blueprint('user_route', __name__)

@user_route.route("/")
def user_dashboard():
    return render_template("user_templates/index.html")

@user_route.route("/greenhouse")
def greenhouse():
    default_plants = get_default_plants()
    return render_template("user_templates/greenhouse-page.html", default_plants = default_plants)

@user_route.route("/add_default_plant")
def add_default_plant():
    plant_code = request.form.get()
    user_id = session.get("USER_LOGGED_IN")['id']
    
@user_route.route("/add_custom_plant")
def add_custom_plant():
    return "<h1>Nyah</h1>"