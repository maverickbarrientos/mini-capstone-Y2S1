import json
import serial
import time
import atexit
from flask import current_app

arduino = None
try:
    arduino = serial.Serial('COM4', 9600, timeout=5)
    time.sleep(2)
except Exception as e:
    print(f"Error : {e}")

arduino.reset_input_buffer()
arduino.reset_output_buffer()

def fetch_pins_arduino():
    arduino.write(b'FETCH_PINS')
    pins = arduino.readline().decode().strip()
    print(pins)
    try:
        data = json.loads(pins)
        print("yamte")
        return data
    except Exception as e:
        import traceback
        print("kudasai")
        traceback.print_exc()
        print(f"Error : {e}")
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
    pin_list = [pin for pin in pins]
    watering_pins = json.dumps(pin_list)
    command = f"WATER:{watering_pins}\n".encode()
    arduino.write(command)

def close_connection():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        print("Arduino connection closed.")

atexit.register(close_connection)