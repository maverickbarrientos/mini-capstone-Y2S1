from models.user_models.greenhouse_model import update_watered_plant, get_user_plants
from arduino import water_arduino
import threading, schedule, time

started = {}
threads = {}
stop_events = {}

def watering_logic(weather_forecast, user_id):
    
    water = []
    plants = get_user_plants(user_id)
            
    for plant in plants:
        print(plant)
        temp = round(weather_forecast['main']['temp'] - 273.15, 1)
        ideal_max_temp = float(plant['custom_plants.ideal_max_temp'] if plant['custom_plants.ideal_max_temp'] else plant['ideal_max_temp'])
        if temp > ideal_max_temp:
            print("hahahhaa", plant['sensor_pin'])
            water.append(plant['sensor_pin'])
            update_watered_plant(plant['plant_id'], plant['sensor_pin'])

            
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
        