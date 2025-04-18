import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='gunn',
        password='password123',
        database='cloud_storage'
    )
    print("Connection successful!")
    connection.close()
except Exception as e:
    print("Connection failed:", e)
