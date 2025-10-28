from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def get_total_users():
    try:
        sql = "SELECT COUNT(*) FROM user_accounts"
        cursor.execute(sql)
        result = cursor.fetchone()['COUNT(*)']
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def user_stats():
    try:
        sql = """SELECT 
            MONTH(created_at) AS month,
            COUNT(*) AS count
            FROM user_accounts
            GROUP BY MONTH(created_at)
            ORDER BY MONTH(created_at)"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def plant_stats():
    cursor.execute("""
        SELECT dp.plant_name, COUNT(up.id) AS count
        FROM user_plants AS up
        JOIN default_plants AS dp ON up.plant_id = dp.id
        WHERE dp.is_default = 1
        GROUP BY dp.plant_name
        ORDER BY count DESC
    """)
    result = cursor.fetchall()
    return result
    
def total_default_plants():
    try:
        sql = "SELECT COUNT(*) FROM default_plants"
        cursor.execute(sql)
        result = cursor.fetchone()['COUNT(*)']
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def total_custom_plants():
    try:
        sql = "SELECT COUNT(*) FROM custom_plants"
        cursor.execute(sql)
        result = cursor.fetchone()['COUNT(*)']
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def total_issues():
    try:
        sql = "SELECT COUNT(*) FROM custom_plants"
        cursor.execute(sql)
        result = cursor.fetchone()['COUNT(*)']
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def get_common_plants():
    sql_user_plants = "SELECT plant_id, COUNT(*) AS total FROM user_plants GROUP BY plant_id ORDER BY total DESC LIMIT 5;"
    cursor.execute(sql_user_plants)
    result = cursor.fetchone()['COUNT(*)']
    print(result)