from flask import Blueprint, render_template, jsonify, request, url_for, redirect, session, flash
from models.admin.dashboard_model import get_total_users, total_custom_plants, total_default_plants, total_issues
from models.admin.user_model import get_users, get_user_data, update_user_process, delete_user_process
from models.admin.plant_model import get_plants, get_plant_data, update_plant_process, delete_plant_process
from services.admin_services import newUser, newPlant

admin_route = Blueprint("admin_route", __name__)

#USER ROUTE
@admin_route.route("/")
def admin_dashboard():
    total_users = get_total_users()
    default_plants = total_default_plants()
    custom_plants = total_custom_plants()
    issues_reported = total_issues()
    return render_template("admin/index.html", total_users = total_users, custom_plants = custom_plants, default_plants = default_plants, issues_reported = issues_reported)

#CREATE
@admin_route.route("/add_user_template")
def add_user_template():
    return render_template("admin/users/add-user.html")

@admin_route.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        new_user = newUser(request.form)
        insert = new_user.insert_user()
        print(insert)
        return redirect(url_for('admin_route.user_management')) 
    
#READ
@admin_route.route("/user_management")
def user_management():
    users = get_users()
    print(users)
    return render_template('admin/users/index.html', users = users)

#UPDATE
@admin_route.route("/user_action_process", methods=["POST"])
def user_action_process():
    id = request.form.get("id-input")
    button = request.form.get("action-btn")
    
    if button == "update-btn":
        return redirect(url_for('admin_route.get_user', id = id))
    elif button == "delete-btn":
        return redirect(url_for('admin_route.delete_user', id = id))
    
@admin_route.route("/get_user")
def get_user():
    id = request.args.get("id")
    user = get_user_data(id) #GET USER FUNCTION
    return render_template("admin/users/update.html", user_data = user)

@admin_route.route("/update_user", methods=["POST", "GET"])
def update_user():
    if request.method == "POST":
        id = request.form.get("id-input")
        first_name = request.form.get("first-name-input")
        last_name = request.form.get("last-name-input")
        birthdate = request.form.get("birthdate-input")
        email = request.form.get("email-input")
        phone_number = request.form.get("phone-number-input")
        
        update_user_process(first_name, last_name, birthdate, email, phone_number, id) #UPDATE USER FUNCTION
        
        return redirect(url_for('admin_route.user_management'))

#DELETE
@admin_route.route("/delete_user")
def delete_user():
    id = request.args.get("id")
    delete_user_process(id) #DELETE FUNCTION
    return redirect(url_for('admin_route.user_management'))

#PLANT ROUTES
@admin_route.route("/plant_management", methods=["POST", "GET"])
def plant_management():
    plants = get_plants()
    return render_template('admin/plants/index.html', plants = plants)

@admin_route.route("/add_plant_template")
def add_plant_template():
    return render_template("admin/plants/add-plant.html")

@admin_route.route("/add_plant", methods=["POST"])
def add_plant():
    new = newPlant(request.form)
    new.insert_plant()
    return redirect(url_for('admin_route.plant_management'))

@admin_route.route("/plant_action_process", methods=["POST"])
def plant_action_process():
    id = request.form.get("id-input")
    button = request.form.get("action-btn")
    
    if button == "update-btn":
        return redirect(url_for('admin_route.get_plant', id = id))
    else:
        return redirect(url_for('admin_route.delete_plant', id = id))
    
@admin_route.route("/get_plant")
def get_plant():
    id = request.args.get("id")
    plant = get_plant_data(id)
    print(plant)
    return render_template('admin/plants/update.html', plant_data = plant)

@admin_route.route("/update_plant", methods=["POST"])
def update_plant():
    id = request.form.get("id-input")
    plant_name = request.form.get("plant-name-input")
    description = request.form.get("description-input")
    soil_type = request.form.get("soil-type-input")
    water_amount = request.form.get("water-amount-input")
    min_moisture = request.form.get("min-moisture-input")
    max_moisture = request.form.get("max-moisture-input")
    min_temp = request.form.get("min-temp-input")
    max_temp = request.form.get("max-temp-input")
    
    update_plant_process(id, plant_name, description, soil_type, water_amount, min_moisture, max_moisture, min_temp, max_temp)
    
    return redirect(url_for("admin_route.plant_management"))

@admin_route.route("/delete_plant")
def delete_plant():
    id = request.args.get("id")
    delete_plant_process(id)
    flash(message="Delete Successful")
    return redirect(url_for('admin_route.plant_management'))