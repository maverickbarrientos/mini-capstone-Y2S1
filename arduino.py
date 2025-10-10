import json
import serial
import time

arduino = None
try:
    arduino = serial.Serial('COM4', 9600, timeout=5)
    time.sleep(2)
except Exception as e:
    print(f"Error : {e}")

arduino.reset_input_buffer()
arduino.reset_output_buffer()

def fetch_pins_arduino():
    arduino.write(b'B')
    pins = arduino.readline().decode().strip()
    try:
        data = json.loads(pins)
        return data
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error : {e}")
        return None

def set_pin_arduino(pin):
    command = f"A{pin}\n".encode()
    arduino.write(command)
    print(command)
    return {"status" : True}

def get_reserved_pins_arduino():
    arduino.write(b'C')
    pins = arduino.readline().decode().strip()
    data = json.loads(pins)
    return data

def release_pin_arduino(pin):
    command = f"D{pin}\n".encode()
    arduino.write(command)
    print(command)
    return {'status' : True}

def update_pins_arduino(reserved_pin):
    pin_list = json.dumps(reserved_pin)
    command = f"E{pin_list}\n".encode()
    arduino.write(command)
    return {'status' : 'Updated'}

import atexit

def close_connection():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        print("Arduino connection closed.")

atexit.register(close_connection)