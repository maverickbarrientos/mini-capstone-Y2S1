import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='P@$$w0rd',
        db='plant_pulse_db',
        cursorclass = pymysql.cursors.DictCursor,
        autocommit=True
    )