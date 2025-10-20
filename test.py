from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def get_common_plants():
    sql_user_plants = """SELECT user_plants.plant_code, COALESCE(default_plants.plant_name, custom_plants.plant_name) AS plant_name,
    COUNT(*) AS total
    FROM user_plants
    LEFT JOIN default_plants ON default_plants.plant_code = user_plants.plant_code
    LEFT JOIN custom_plants ON custom_plants.plant_code = user_plants.plant_code
    GROUP BY user_plants.plant_code 
    ORDER BY total DESC 
    LIMIT 5;"""
    cursor.execute(sql_user_plants)
    result = cursor.fetchall()
    print(result)
    
get_common_plants()