from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def get_reports():
    try:
        sql = "SELECT * FROM support_and_issues"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def get_user_report(id):
    try:
        sql = "SELECT * FROM support_and_issues WHERE id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def update_status(id, status):
    try:
        sql = "UPDATE support_and_issues SET status = %s WHERE id =%s"
        cursor.execute(sql, (status, id))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None

def delete_report(id):
    try:
        sql = "DELETE FROM support_and_issues WHERE id =%s"
        cursor.execute(sql, (id, ))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None