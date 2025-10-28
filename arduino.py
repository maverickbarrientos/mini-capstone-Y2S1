import json
import serial
import time
import atexit
from flask import current_app
import threading

arduino = None
serial_lock = threading.Lock()

try:
    arduino = serial.Serial('COM4', 9600, timeout=5)
    time.sleep(2)
except Exception as e:
    print(f"Error : {e}")

arduino.reset_input_buffer()
arduino.reset_output_buffer()

def fetch_pins_arduino():
    with serial_lock:
        arduino.reset_input_buffer()
        arduino.write(b'FETCH_PINS\n')
        arduino.flush()

        pins = ""
        start_time = time.time()
        timeout = 2  # seconds

        while True:
            if arduino.in_waiting > 0:
                read = arduino.readline().decode(errors='ignore').strip()
                if read:
                    pins = read
                    break

            if time.time() - start_time > timeout:
                print("Timeout while waiting for Arduino response.")
                break

            time.sleep(0.01)  # fast but safe polling

        if not pins:
            print("No response from Arduino.")
            return None

        try:
            data = json.loads(pins)
            print("yamte")  # for debugging
            return data
        except Exception as e:
            import traceback
            print("kudasai")
            traceback.print_exc()
            print(f"Error: {e}")
            print("Raw data:", pins)
            return None

def set_pin_arduino(pin):
    command = f"RESERVE_PIN:{pin}\n".encode()
    arduino.write(command)
    print(command)
    return {"status" : True}

def get_reserved_pins_arduino():
    arduino.write(b'GET_RESERVED_PINS')
    pins = arduino.readline().decode().strip()
    data = json.loads(pins)
    return data

def release_pin_arduino(pin):
    command = f"RELEASE_PIN:{pin}\n".encode()
    arduino.write(command)
    print(command)
    return {'status' : True}

def pins_to_read(pins):
    arduino.reset_input_buffer()
    pin_list = [str(pin['sensor_pin']) for pin in pins]
    read_pins = json.dumps(pin_list)
    command = f"READ:{read_pins}\n".encode()
    arduino.write(command)
    readings = arduino.readline().decode().strip()
    
    while not readings:
        readings = arduino.readline().decode().strip() 
       
    data = json.loads(readings)
    return data

def water_arduino(pins):
    watering_list = [{"pins" : sensor, "time" : time} for sensor, time in pins.items()]
    watering_pins = json.dumps(watering_list)
    print(pins, watering_pins)
    command = f"WATER:{watering_pins}\n".encode()
    arduino.write(command)

def close_connection():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        print("Arduino connection closed.")

atexit.register(close_connection)