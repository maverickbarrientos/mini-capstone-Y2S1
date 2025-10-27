from flask import jsonify, flash
from db import get_connection
from datetime import date
import random
from abc import ABC, abstractmethod
import string

connection = get_connection()
cursor = connection.cursor()

def get_current_date():
    return date.today()

class newUser():
    def __init__(self, form):
        self.first_name = form.get("first-name-input")
        self.last_name = form.get("last-name-input")
        self.birthdate = form.get("birthdate-input")
        self.email = form.get("email-input")
        self.phone_number = form.get("phone-number-input")
        self.password = form.get("password-input")
        self.profile_picture = form.get("profile_picture")
        
    def find_duplicate(self):
        sql_duplicate = """
            SELECT * FROM user_details WHERE first_name = %s AND last_name = %s AND birthdate = %s AND email = %s;
        """
        cursor.execute(sql_duplicate, (self.first_name, self.last_name, self.birthdate, self.email))
        duplicate = cursor.fetchone()
        return duplicate
    
    def insert_user(self):
        duplicate = self.find_duplicate()
                
        if duplicate is None:
            try:
                sql_insert = """
                INSERT INTO user_details(first_name, last_name, birthdate, email, phone_number, profile_picture)   
                VALUES (%s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql_insert, (self.first_name, self.last_name, self.birthdate, self.email, self.phone_number, self.profile_picture))
                connection.commit()
                
                user_id = cursor.lastrowid 
                
                sql_insert_account = """
                    INSERT INTO user_accounts(user_id, email, password, created_at)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(sql_insert_account, (user_id, self.email, self.password, get_current_date()))
                connection.commit()
                return None
            except Exception as e:
                print(f"Error : {e}")
                return None
        
            
class plant():
    def __init__(self, form):
        self.plant_name = form.get("plant-name-input")
        self.description = form.get("description-input")
        self.water_amount = form.get("water-amount-input")
        self.soil_type = form.get("soil-type-input") 
        self.min_moisture = form.get("min-moisture-input")
        self.max_moisture = form.get("max-moisture-input")
        self.min_temp = form.get("min-temp-input")
        self.max_temp = form.get("max-temp-input")
    
    @abstractmethod
    def insert_plant(self):
        pass
        
class newPlant(plant):
    def __init__(self, form):
        super().__init__(form)

    def insert_plant(self):
        try:
            sql_insert_plant = """
                INSERT INTO default_plants(plant_name, description, soil_type, optimal_water_amount, soil_min_moisture, soil_max_moisture, ideal_min_temp, ideal_max_temp)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_plant, (self.plant_name, self.description, self.soil_type, self.water_amount, self.min_moisture, self.max_moisture, self.min_temp, self.max_temp))
            
            id = cursor.lastrowid
            code = generate_code(id, self.plant_name)
            sql_plant_code = """
                UPDATE default_plants SET plant_code = %s WHERE id = %s;
            """
            cursor.execute(sql_plant_code, (code, id))
            
            connection.commit()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error : {e}")
            return None
        
class customPlant(newPlant):
    def __init__(self, form, user_id):
        super().__init__(form)
        self.user_id = user_id
        
    def insert_plant(self):
        try:
            sql_insert_plant = """
                INSERT INTO custom_plants(created_by, plant_name, description, soil_type, optimal_water_amount, soil_min_moisture, soil_max_moisture, ideal_min_temp, ideal_max_temp)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_plant, (self.user_id ,self.plant_name, self.description, self.soil_type, self.water_amount, self.min_moisture, self.max_moisture, self.min_temp, self.max_temp))
            
            id = cursor.lastrowid
            
            code = generate_code(id, self.plant_name)
            sql_plant_code = """
                UPDATE custom_plants SET plant_code = %s WHERE id = %s;
            """
            cursor.execute(sql_plant_code, (code, id))
            connection.commit()
            return id
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error : {e}")
            return None

class newReport(): 
    def __init__(self, form, user_id):
        self.user_id = user_id
        self.name = form.get("name-input")
        self.email = form.get("email-input")
        self.issue = form.get("issue")

    def existing_report(self):
        try:
            sql = "SELECT * FROM support_and_issues WHERE user_id = %s"
            cursor.execute(sql, (self.user_id))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error : {e}")
            return None
        
    def add_report(self):
        existing_report = self.existing_report
        
        if existing_report is not None:
            try:
                sql = """INSERT INTO support_and_issues(sender_id, sender_name, sender_email, issue_description, created_at)
                        VALUES(%s, %s, %s, %s, %s)
                        """
                cursor.execute(sql, (self.user_id, self.name, self.email, self.issue, get_current_date()))
                connection.commit()
                return {'status' : True}
            except Exception as e:
                print(f"Error : {e}")
                return None
        else:
            flash("Report already exists!")
            return None

def generate_code(id, plant_name):
    print(plant_name)
    
    prefix = " "
    for i in range(3):
        prefix += plant_name[i]
    
    random_part = ''.join(random.choices(string.ascii_uppercase, k=3))
        
    code = f"{prefix.upper()}-{random_part}-{id:03d}"
    return code

def normalize_plants(raw_plants):
    normalized = []
    for plant in raw_plants:
        if plant['custom_plants.id']:
            normalized.append({
                'user_plant_id': plant['user_plants.id'],
                'plant_id': plant['custom_plants.id'],
                'plant_name': plant['custom_plants.plant_name'],
                'plant_code': plant['custom_plants.plant_code'],
                'description': plant['custom_plants.description'],
                'soil_type': plant['custom_plants.soil_type'],
                'optimal_water_amount': plant['custom_plants.optimal_water_amount'],
                'soil_min_moisture': plant['custom_plants.soil_min_moisture'],
                'soil_max_moisture': plant['custom_plants.soil_max_moisture'],
                'ideal_min_temp': plant['custom_plants.ideal_min_temp'],
                'ideal_max_temp': plant['custom_plants.ideal_max_temp'],
                'is_default': False,
                'sensor_name': plant['sensor_name'],
                'sensor_pin': plant['sensor_pin'],
                'sensor_status': plant['sensor_status'],
                'moisture_level': plant['moisture_level'],
                'watering_status': plant['watering_status'],
                'last_watered': plant['last_watered'],
                'plant_photo': plant['plant_photo']
            })
        else:
            normalized.append({
                'user_plant_id': plant['user_plants.id'],
                'plant_id': plant['plant_id'],
                'plant_name': plant['plant_name'],
                'plant_code': plant['plant_code'],
                'description': plant['description'],
                'soil_type': plant['soil_type'],
                'optimal_water_amount': plant['optimal_water_amount'],
                'soil_min_moisture': plant['soil_min_moisture'],
                'soil_max_moisture': plant['soil_max_moisture'],
                'ideal_min_temp': plant['ideal_min_temp'],
                'ideal_max_temp': plant['ideal_max_temp'],
                'is_default': True,
                'sensor_name': plant['sensor_name'],
                'sensor_pin': plant['sensor_pin'],
                'sensor_status': plant['sensor_status'],
                'moisture_level': plant['moisture_level'],
                'watering_status': plant['watering_status'],
                'last_watered': plant['last_watered'],
                'plant_photo': plant['plant_photo']
            })
    return normalized
    