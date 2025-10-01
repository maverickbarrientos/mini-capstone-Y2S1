from flask import jsonify
from db import get_connection
from datetime import date

connection = get_connection()
cursor = connection.cursor()

def get_current_date():
    current_date = date.today()
    return current_date

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
                return jsonify({"successful" : "True"})
            except Exception as e:
                return jsonify({"error inserting" : e})
        else:
            return jsonify({"successful" : "False"})