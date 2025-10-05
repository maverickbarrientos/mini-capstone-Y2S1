from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def get_plants():
    sql_get_plants = "SELECT * FROM default_plants"
    cursor.execute(sql_get_plants)
    plants = cursor.fetchall()
    return plants

def get_plant_data(id):
    sql_get_plant = "SELECT * FROM default_plants WHERE id = %s"
    cursor.execute(sql_get_plant, (id,))
    plant = cursor.fetchone()
    return plant

def update_plant_process(id, plant_name, description, soil_type, water_amount, min_moisture, max_moisture, min_temp, max_temp):
    try:
        sql_update = """UPDATE default_plants 
                SET plant_name = %s, description = %s, soil_type = %s, optimal_water_amount = %s, soil_min_moisture = %s, soil_max_moisture = %s, 
                ideal_min_temp = %s, ideal_max_temp = %s WHERE id = %s;
        """
        cursor.execute(sql_update, (plant_name, description, soil_type, water_amount, min_moisture, max_moisture, min_temp, max_temp, id))
        connection.commit()
        print("Apdit Saksis")
    except Exception as e:
        print(f"Failed updating : {e}")
        
def delete_plant_process(id):
    try:
        sql_delete = "DELETE FROM default_plants WHERE id = %s"
        cursor.execute(sql_delete, (id, ))
        connection.commit()
    except Exception as e:
        print(f"Error : {e}")
        return None    
