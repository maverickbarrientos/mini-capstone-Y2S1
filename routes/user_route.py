from flask import Blueprint, redirect, render_template, url_for, request, session, jsonify
from models.user_models.greenhouse_model import get_default_plants, get_pins_db, get_chosen_plants, new_plant, get_reserved_pins, remove_pin, get_reserved_pins
from arduino import fetch_pins_arduino, set_pin_arduino, get_reserved_pins_arduino, release_pin_arduino, update_pins_arduino

user_route = Blueprint('user_route', __name__)

@user_route.route("/")
def user_dashboard():
    return render_template("user_templates/index.html")

@user_route.route("/greenhouse")
def greenhouse():
    default_plants = get_default_plants()
    return render_template("user_templates/greenhouse-page.html", default_plants = default_plants)

@user_route.route("/add_default_plant", methods=["POST"])
def add_default_plant():
    id = request.form.getlist("plant_checkbox")
    plants = get_chosen_plants(tuple(id))
    reserved_pins = get_reserved_pins()
    print(reserved_pins)
    print(plants)
    return render_template('user_templates/set-pin.html', plants = plants, reserved_pins = reserved_pins)
    
@user_route.route("/add_custom_plant")
def add_custom_plant():
    return "<h1>Nyah</h1>"

@user_route.route("/fetch_pins")
def fetch_pins():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    reserved_pin_list = get_reserved_pins(user_id)
    reserved_pins = [int(pin['pin_number']) for pin in reserved_pin_list]
    update_pins_arduino(reserved_pins)
    data = fetch_pins_arduino()
    return jsonify(data)

@user_route.route("/set_pin_process", methods=["POST", "GET"])
def set_pin_process():
    data = request.get_json()
    pin = data.get("pin")
    plant_id = data.get("currentPlant")
    user_id = session.get("USER_LOGGED_IN")['user_id']
    print(user_id)
    sensor_name = data.get("sensorName")
    
    new_plant(user_id, plant_id, sensor_name, pin)
    set_pin_arduino(pin)
    
    return jsonify({"status" : True})

@user_route.route("/release_pin", methods=["POST"])
def release_pin():
    data = request.get_json()
    pin = data.get("pin")
    plantId = data.get("plantId")
    release_pin_arduino(pin)
    remove_pin(plantId)
    return jsonify({'status' : 'success'})