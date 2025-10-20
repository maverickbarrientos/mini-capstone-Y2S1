from models.user_models.greenhouse_model import update_watered_plant
from arduino import water_arduino
import threading, schedule, time

started = {}

watering_scheduler = schedule.Scheduler()

def watering_logic(weather_forecast, plants):
    
    water = []
        
    for plant in plants:
        temp = round(weather_forecast['main']['temp'] - 273.15, 1)
        ideal_max_temp = float(plant['ideal_max_temp'])
        print(temp)
        print(ideal_max_temp)
        if temp < ideal_max_temp:
            water.append(plant['sensor_pin'])
            update_watered_plant(plant['plant_id'], plant['sensor_pin'])
            
    water_arduino(water)
    
def run_countdown():
    while True:
        watering_scheduler.run_pending()
        time.sleep(1)

def start_watering(weather_forecast, plants, user_id):
    global started
    if user_id in started:
        return
    
    started[user_id] = True
    watering_scheduler.every(15).seconds.do(lambda: watering_logic(weather_forecast, plants))
    threading.Thread(target=run_countdown, daemon=True).start()