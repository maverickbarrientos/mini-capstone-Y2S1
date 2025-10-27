import json
from flask import Blueprint, current_app, flash, redirect, render_template, url_for, request, session, jsonify, current_app
from models.user_models.greenhouse_model import get_custom_plant, get_default_plants, get_chosen_plants, new_plant, get_reserved_pins, remove_pin, update_custom_plant, update_custom_sensor, update_watered_plant, user_reserved_pins, get_user_plants, get_plant, update_default_plant, delete_plant
from models.user_models.user_model import get_user, get_number_of_plants, update_photo, update_user
from arduino import fetch_pins_arduino, set_pin_arduino, get_reserved_pins_arduino, release_pin_arduino, pins_to_read, water_arduino
from services.entity_services import customPlant, newPlant, newReport, normalize_plants
from services.sensor_service import start
from services.weather_service import get_forecast, get_latest_forecast
from services.watering_service import watering_logic, start_watering, stop_watering
import time, threading, schedule
import os

user_route = Blueprint('user_route', __name__)    

@user_route.route("/")
def user_dashboard():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    if "USER_LOGGED_IN" in session:
        user = get_user(user_id)
        raw_plants = get_user_plants(user_id)
        plants = normalize_plants(raw_plants)
        return render_template("user_templates/index.html", user = user, plants = plants)
    return redirect(url_for('main.login'))

@user_route.route("/get_coords", methods=["POST"])
def get_coords():
    data = request.get_json()
    lat = data.get("latitude")
    long = data.get("longitude")
    forecast = get_latest_forecast(lat, long)
    return jsonify({'forecast' : forecast})

@user_route.route("/default_plant", methods=["POST", "GET"])
def default_plant():
    default_plants = get_default_plants()
    user_id = session.get("USER_LOGGED_IN")['user_id']
    user = get_user(user_id)
    return render_template("user_templates/add-plant.html", default_plants = default_plants, user = user)

@user_route.route("/greenhouse")
def greenhouse():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    raw_plants = get_user_plants(user_id)
    user = get_user(user_id)
    plants = normalize_plants(raw_plants)
    return render_template("user_templates/greenhouse.html", plants = plants, user = user)

@user_route.route("/watering_mode", methods=["POST"])
def watering_mode():
    data = request.get_json()
    mode = data.get("mode")
    return jsonify({'mode' : mode})

@user_route.route("/automatic_watering", methods=["POST", "GET"])
def automatic_watering():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    start(user_id)
    data = request.get_json()
    longitude = data.get("longitude")
    latitude = data.get("latitude")
    forecast = get_forecast(latitude, longitude)
    start_watering(forecast, user_id)
    return jsonify({"maverick" : "gwapo"})

@user_route.route("/manual_watering", methods=["POST", "GET"])
def manual_watering():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    stop_watering(user_id)
    data = request.get_json()
    plants = data.get("plants")
    for plant in plants:
        water_arduino(plant["sensorPin"])
        update_watered_plant(plant["plantId"], plant["sensorPin"])
    return jsonify({'plant' : plant})

@user_route.route("/add_default_plant", methods=["POST"])
def add_default_plant():
    id = request.form.getlist("plant_checkbox")
    plants = get_chosen_plants(tuple(id))
    user_id = session.get("USER_LOGGED_IN")['user_id']
    user = get_user(user_id)
    if plants:
        reserved_pins = get_reserved_pins()
        return render_template('user_templates/set-pin.html', plants = plants, reserved_pins = reserved_pins, user = user)
    else:
        flash("Select a plant first")
        return redirect(url_for('user_route.default_plant'))
    
@user_route.route("/custom_plant")
def custom_plant():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    user = get_user(user_id)
    return render_template("user_templates/add-custom-plant.html", user = user)

@user_route.route("/add_custom_plant", methods=["POST"])
def add_custom_plant():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    new = customPlant(request.form, user_id)
    user = get_user(user_id)
    insert = new.insert_plant()
    plant = get_custom_plant(insert)
    reserved_pins = get_reserved_pins()
    return render_template('user_templates/custom-plant-pin.html', plant = plant, reserved_pins = reserved_pins, user = user)

@user_route.route("/fetch_pins")
def fetch_pins():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    data = fetch_pins_arduino()
    return jsonify(data)

@user_route.route("/set_pin_process", methods=["POST", "GET"])
def set_pin_process():
    pin = request.form.get("pin")
    plant_id = request.form.get("currentPlant")
    user_id = session.get("USER_LOGGED_IN")['user_id']
    sensor_name = request.form.get("sensorName")
    image = request.files.get("image")
    
    if image:
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], image.filename)
        image.save(filepath)
        plant_photo = "plant_images/" + image.filename
    else:
        plant_photo = "plant_images/default_img.jpg"
        
    new_plant(user_id, plant_id, sensor_name, pin, plant_photo)
    set_pin_arduino(pin)
    
    return jsonify({"status" : True})

@user_route.route("/release_pin", methods=["POST"])
def release_pin():
    data = request.get_json()
    pin = data.get("pin")
    plantId = data.get("plantId")
    user_id = session.get("USER_LOGGED_IN")['user_id']
    release_pin_arduino(pin)
    remove_pin(plantId, user_id)
    return jsonify({'status' : 'success'})

@user_route.route("/report_issues")
def report_issues():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    user = get_user(user_id)
    return render_template('user_templates/report-issues.html', user = user)

@user_route.route("/submit_report", methods=["POST"])
def submit_report():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    new_report = newReport(request.form, user_id)
    new_report.add_report()    
    return redirect(url_for('user_route.report_issues'))

@user_route.route("/plant_information/<string:id>")
def plant_information(id):
    plant = get_plant(id)
    return jsonify({'plant' : plant})

@user_route.route("/action/<string:id>", methods=["POST"])
def action(id):
    action = request.form.get("action")
    sensor_pin = request.form.get("select-pin")
    plant_name = request.form.get("custom-plant-name")
    soil_type = request.form.get("soil-type")
    description = request.form.get("description")
    water_amount = request.form.get("optimal-water-amount")
    min_moisture = request.form.get("soil-min-moisture")
    max_moisture = request.form.get("soil-max-moisture")
    min_temp = request.form.get("ideal-min-temp")
    max_temp = request.form.get("ideal-max-temp")
    sensor_pin = request.form.get("select-pin")
    plant_id = get_custom_plant(id)
    file = request.files.get("plant-photo")
    is_default = request.form.get("is-default")
    
    print(description, min_temp, max_temp)
    
    if action == "update":
        if is_default is None:
            update_custom_sensor(id, sensor_pin)
            update_custom_plant(plant_id, plant_name, description, soil_type, water_amount, min_moisture, max_moisture, min_temp, max_temp)
            print("aylabyu")
        else:
            
            if file:
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                plant_photo = "plant_images/" + file.filename
            else:
                plant_photo = "plant_images/default_img.jpg"
            
            update_default_plant(sensor_pin, id, plant_photo)
            set_pin_arduino(sensor_pin)
    elif action == "delete":
        delete_plant(id)

    return redirect(url_for('user_route.greenhouse'))

@user_route.route("/profile/<string:user_id>")
def profile(user_id):
    user_information = get_user(user_id)
    plants = get_number_of_plants(user_id)
    return render_template('user_templates/profile.html', user = user_information, plants = plants)

@user_route.route("/update_profile_picture/<string:user_id>", methods=["POST", "GET"])
def update_profile_picture(user_id):
    image = request.files.get("image")
    
    if image:
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], image.filename)
        image.save(filepath)
        profile_photo = "plant_images/" + image.filename
        update_photo(profile_photo, user_id)
        
    return jsonify({'ako ni' : 'natoy'})

@user_route.route("/edit_profile/<string:user_id>")
def edit_profile(user_id):
    user = get_user(user_id)
    return jsonify({'user' : user})

@user_route.route("/update_profile/<string:user_id>", methods=["POST"])
def update_profile(user_id):
    first_name = request.form.get("first-name-input")
    last_name = request.form.get("last-name-input")
    email = request.form.get("email-input")
    phone_number = request.form.get("phone-number-input")
    birthdate = request.form.get("birthdate-input")
    update_user(first_name, last_name, email, phone_number, birthdate, user_id)
    return redirect(url_for('user_route.profile', user_id = user_id))