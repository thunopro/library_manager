import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load cấu hình từ file .env
load_dotenv()

def create_connection():
    """Tạo kết nối đến MySQL database"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        # print("Kết nối MySQL thành công") # Chỉ bật khi cần debug
    except Error as e:
        print(f"Lỗi kết nối '{e}'")
    
    return connection

# print (os.getenv("DB_PASSWORD"))
# print ("Success")