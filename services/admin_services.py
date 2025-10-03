from flask import jsonify
from db import get_connection
from datetime import date
import random
import string

connection = get_connection()
cursor = connection.cursor()

def get_current_date():
    return date.today()

class newUser():
    
    def __init__(self, form):
        self.first_name = form.get("first_name")
        self.last_name = form.get("last_name")
        self.birthdate = form.get("birthdate")
        self.email = form.get("email")
        self.phone_number = form.get("phone_number")
        self.password = form.get("password")
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
        print("PERS NAME", self.first_name)
        
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
                return jsonify({"successful" : True})
            except Exception as e:
                return jsonify({"error inserting" : str(e)})
        else:
            return jsonify({"successful" : False})
        
class newPlant():
    def __init__(self, form):
        self.plant_code = form.get("plant_code")
        self.plant_name = form.get("plant-name-input")
        self.description = form.get("description-input")
        self.soil_type = form.get("soil-type-input")
        self.water_amount = form.get("water-amount-input")
        self.min_moisture = form.get("min-moisture-input")
        self.max_moisture = form.get("max-moisture-input")
        self.min_temp = form.get("min-temp-input")
        self.max_temp = form.get("max-temp-input")

    def insert_plant(self):
        try:
            print(self.plant_name)
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


def generate_code(id, plant_name):
    print(plant_name)
    
    prefix = " "
    for i in range(3):
        prefix += plant_name[i]
    
    random_part = ''.join(random.choices(string.ascii_uppercase, k=3))
        
    code = f"{prefix.upper()}-{random_part}-{id:03d}"
    return code
    