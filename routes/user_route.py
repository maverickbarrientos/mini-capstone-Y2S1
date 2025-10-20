from flask import Blueprint, redirect, render_template, url_for, request, session, jsonify
from models.user_models.greenhouse_model import get_default_plants, get_chosen_plants, new_plant, get_reserved_pins, remove_pin, user_reserved_pins, get_user_plants, update_plant_moisture
from arduino import fetch_pins_arduino, set_pin_arduino, get_reserved_pins_arduino, release_pin_arduino, pins_to_read
import time, threading, schedule

user_route = Blueprint('user_route', __name__)
started = {}

def read_sensor(plants, user_id):
    readings = pins_to_read(plants)
    print(plants)
    print(readings)
    
    for plant in plants:
        if plant['sensor_pin'] in readings:
            update_plant_moisture(readings[plant["sensor_pin"]], user_id, plant['plant_id'])
            print(f"Updating plant {plant['plant_id']} with value {readings[plant['sensor_pin']]}")
            
def schedule_reading(user_id):
    plants = get_user_plants(user_id)
    read_sensor(plants, user_id)

def run_read_sensor():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
def start(user_id):
    global started
    if user_id in started:
        return
    
    started[user_id] = True
    schedule.every(10).seconds.do(lambda: schedule_reading(user_id))
    schedule_reading(user_id)
    threading.Thread(target=run_read_sensor, daemon=True).start()
    

@user_route.route("/")
def user_dashboard():
    return render_template("user_templates/index.html")

@user_route.route("/add_plant", methods=["POST", "GET"])
def plant_status():
    default_plants = get_default_plants()
    return render_template("user_templates/add-plant.html", default_plants = default_plants)

@user_route.route("/greenhouse")
def greenhouse():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    plants = get_user_plants(user_id)
    start(user_id)
    return render_template("user_templates/greenhouse.html", plants = plants)

@user_route.route("/add_default_plant", methods=["POST"])
def add_default_plant():
    id = request.form.getlist("plant_checkbox")
    plants = get_chosen_plants(tuple(id))
    reserved_pins = get_reserved_pins()
    return render_template('user_templates/set-pin.html', plants = plants, reserved_pins = reserved_pins)
    
@user_route.route("/add_custom_plant")
def add_custom_plant():
    return "<h1>Nyah</h1>"

@user_route.route("/fetch_pins")
def fetch_pins():
    user_id = session.get("USER_LOGGED_IN")['user_id']
    reserved_pin_list = user_reserved_pins(user_id)
    data = fetch_pins_arduino()
    return jsonify(data)

@user_route.route("/set_pin_process", methods=["POST", "GET"])
def set_pin_process():
    data = request.get_json()
    pin = data.get("pin")
    plant_id = data.get("currentPlant")
    user_id = session.get("USER_LOGGED_IN")['user_id']
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