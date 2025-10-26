from db import get_connection
from services.entity_services import plant

connection = get_connection()
cursor = connection.cursor()

def get_default_plants():
    try:
        sql = "SELECT * FROM default_plants"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def get_plant(id):
    try:
        sql = """ SELECT default_plants.*, custom_plants.*, user_plants.*
         FROM user_plants
         LEFT JOIN default_plants ON user_plants.plant_id = default_plants.id
         LEFT JOIN custom_plants  ON user_plants.plant_id = custom_plants.id
         WHERE user_plants.plant_id = %s
        """
        cursor.execute(sql, (id, ))
        result = cursor.fetchone()
        print(result)
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_pins_db():
    try:
        sql = """
            SELECT pin_number FROM sensors;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error occured : {e}")
        return None

def get_chosen_plants(plant_id):
    try:
        sql = "SELECT * FROM default_plants WHERE id IN %s"
        cursor.execute(sql, (plant_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_custom_plant(id):
    try:
        sql = "SELECT * FROM custom_plants WHERE id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def new_plant(user_id, plant_id, sensor_name, sensor_pin, plant_photo):
    try:
        sql = "INSERT INTO user_plants(user_id, plant_id, sensor_name, sensor_pin, plant_photo) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, plant_id, sensor_name, sensor_pin, plant_photo))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return {'status' : False}
    
def get_reserved_pins():
    try:
        sql = "SELECT id, sensor_pin FROM user_plants"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def remove_pin(plant_id, user_id):
    try:
        sql = "DELETE FROM user_plants WHERE plant_id = %s AND user_id = %s"
        cursor.execute(sql, (plant_id, user_id))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def user_reserved_pins(user_id):
    try:
        sql = "SELECT sensor_pin FROM user_plants WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return {"status" : False}

def get_user_plants(user_id):
    try:
        sql = """
         SELECT default_plants.*, custom_plants.*, user_plants.*
         FROM user_plants
         LEFT JOIN default_plants ON user_plants.plant_id = default_plants.id
         LEFT JOIN custom_plants  ON user_plants.plant_id = custom_plants.id
         WHERE user_plants.user_id = %s
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def update_plant_moisture(moisture_level, user_id, plant_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = "UPDATE user_plants SET moisture_level = %s WHERE user_id = %s AND plant_id = %s"
        cursor.execute(sql, (moisture_level, user_id, plant_id))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def pins_to_water(user_id):
    try:
        sql = """SELECT default_plants.*, custom_plants.*, user_plants.*
                 FROM user_plants 
                 LEFT JOIN default_plants ON user_plants.plant_id = default_plants.id
                 LEFT JOIN custom_plants  ON user_plants.plant_id = custom_plants.id
                 WHERE user_plants.user_id = %s AND user_plants.moisture_level < COALESCE(default_plants.soil_min_moisture, custom_plants.soil_min_moisture)"""
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def update_watered_plant(plant_id, sensor_pin):
    try:
        print(plant_id, sensor_pin)
        sql = """
            UPDATE user_plants SET last_watered = NOW(), watering_status = 'completed' WHERE id = %s AND sensor_pin = %s;
        """
        cursor.execute(sql, (plant_id, sensor_pin))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def update_default_plant(sensor_pin, id, plant_photo):
    try:
        sql = "UPDATE user_plants SET sensor_pin = %s, plant_photo = %s WHERE id = %s"
        cursor.execute(sql, (sensor_pin, plant_photo, id ))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None

def delete_plant(id):
    try:
        sql = "DELETE FROM user_plants WHERE id = %s"
        cursor.execute(sql, (id, ))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def update_custom_plant(id, plant_name, description, soil_type, optimal_water_amount, min_moisture, max_moisture, ideal_min_temp, ideal_max_temp):
    try:
        sql = """UPDATE custom_plants 
        SET plant_name = %s, description = %s, soil_type = %s, optimal_water_amount = %s, 
        soil_min_moisture = %s, soil_max_moisture = %s, ideal_min_temp = %s, ideal_max_temp = %s
        WHERE id = %s"""
        cursor.execute(sql, (plant_name, description, soil_type, optimal_water_amount, min_moisture, max_moisture, ideal_min_temp, ideal_max_temp, id))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def update_custom_sensor(id, sensor_pin):
    try:
        sql = "UPDATE user_plants SET sensor_pin = %s WHERE id = %s"
        cursor.execute(sql, (sensor_pin, id))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_custom_plant(id):
    try: 
        sql = "SELECT * FROM user_plants WHERE id = %s"
        cursor.execute(sql, (id, ))
        result = cursor.fetchone()
        return result['plant_id']
    except Exception as e:
        print(f"Error : {e}")
        return None