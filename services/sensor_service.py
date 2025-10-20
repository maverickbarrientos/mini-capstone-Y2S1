from arduino import pins_to_read
from models.user_models.greenhouse_model import update_plant_moisture, get_user_plants
import schedule, time, threading

started = {}

sensor_scheduler = schedule.Scheduler()

def read_sensor(plants, user_id):
    readings = pins_to_read(plants)
    
    for plant in plants:
        if plant['sensor_pin'] in readings:
            moisture_level = round(100 - ((readings[plant['sensor_pin']] / 1023) * 100), 1)
            update_plant_moisture(moisture_level, user_id, plant['plant_id'])
            print(f"Updating plant {plant['plant_id']} with value {readings[plant['sensor_pin']]}")
            
def schedule_reading(user_id):
    plants = get_user_plants(user_id)
    read_sensor(plants, user_id)

def run_read_sensor():
    while True:
        sensor_scheduler.run_pending()
        time.sleep(1)
    
def start(user_id):
    global started
    if user_id in started:
        return
    
    started[user_id] = True
    sensor_scheduler.every(10).seconds.do(lambda: schedule_reading(user_id))
    schedule_reading(user_id)
    threading.Thread(target=run_read_sensor, daemon=True).start()