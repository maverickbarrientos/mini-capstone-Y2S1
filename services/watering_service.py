import datetime
from flask import render_template
from flask_mail import Message
import os
from mail_config import mail
from models.user_models.greenhouse_model import update_watered_plant, get_user_plants
from arduino import water_arduino
import threading, schedule, time

from models.user_models.user_model import get_user

started = {}
threads = {}
stop_events = {}

def watering_logic(weather_forecast, user_id):
    
    water = {}
    plants = get_user_plants(user_id)
            
    for plant in plants:
        print(plant)
        temp = round(weather_forecast['main']['temp'] - 273.15, 1)
        weather = weather_forecast['weather'][0]['description']
        
        #PLANT TEMPERATURE
        ideal_max_temp = float(plant['custom_plants.ideal_max_temp'] if plant['custom_plants.ideal_max_temp'] else plant['ideal_max_temp'])
        ideal_min_temp = float(plant['custom_plants.ideal_min_temp'] if plant['custom_plants.ideal_min_temp'] else plant['ideal_min_temp'])
        
        #PLANT SOIL MOISTURE
        min_moisture = float(plant['custom_plants.soil_min_moisture'] if plant['custom_plants.soil_min_moisture'] else plant['soil_min_moisture'])
        max_moisture = float(plant['custom_plants.soil_max_moisture'] if plant['custom_plants.soil_max_moisture'] else plant['soil_max_moisture'])
        current_moisture = float(plant['moisture_level'])
        
        #WATER LEVEL
        #MILILITERS
        water_level = float(plant['custom_plants.optimal_water_amount'] if plant['custom_plants.optimal_water_amount'] else plant['optimal_water_amount'])
        #CONVERT ML TO TIME(MILISECONDS)
        PUMP_PER_SECOND = float(25)
        watering_time = (water_level / PUMP_PER_SECOND) * 1000
        
        raining = "moderate rain" in weather or "heavy rain" in weather
        
        if current_moisture > min_moisture and not raining:
            if temp > ideal_max_temp:
                water[plant['sensor_pin']] = watering_time
                update_watered_plant(plant['plant_id'], plant['sensor_pin'])
            elif ideal_min_temp <= temp <= ideal_max_temp:
                reduced_water = watering_time * 0.75
                water[plant['sensor_pin']] = reduced_water
                update_watered_plant(plant['plant_id'], plant['sensor_pin'])
            elif temp < ideal_min_temp:
                reduced_water = watering_time * 0.50
                water[plant['sensor_pin']] = reduced_water
                update_watered_plant(plant['plant_id'], plant['sensor_pin'])
            
        print(watering_time)
            
    water_arduino(water)
    
def run_countdown(stop_event, watering_scheduler):
    while not stop_event.is_set():
        watering_scheduler.run_pending()
        time.sleep(1)
    print("watering stopped")

def start_watering(weather_forecast, user_id):
    global started
    
    stop_event = threading.Event()
    stop_events[user_id] = stop_event
    
    scheduler = schedule.Scheduler()
    scheduler.every(15).seconds.do(lambda: watering_logic(weather_forecast, user_id))
    send_email(user_id)

    if user_id in started:
        stop_watering(user_id)
    
    thread = threading.Thread(target=run_countdown, args=(stop_event, scheduler), daemon=True)
    thread.start()
    
    started[user_id] = True
    threads[user_id] = thread
    
def stop_watering(user_id):
    global stop_events, threads
    
    if user_id in started:        
        stop_events[user_id].set()
        threads[user_id].join()
        
        del started[user_id]
        del threads[user_id]
        del stop_events[user_id]
        print("Stopped watering for ", user_id)
    else:
        return None
        
def send_email(user_id):    
    user = get_user(user_id)
    plants = get_user_plants(user_id)
    
    watered_plants = [plant for plant in plants if plant['watering_status'] == 'completed']
    watered_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_body = render_template('mail-body.html', user = user, plants = watered_plants, watered_time = watered_time)
    message = Message(subject="Your Plants Have Been Watered 🌱", 
                      sender = os.getenv("EMAIL"), 
                      recipients = [user['email']], 
                      html=html_body)
    mail.send(message)