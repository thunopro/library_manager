import mysql.connector
from app.db.connection import create_connection

class BorrowerModel:
    def get_all_borrowers(self):
        """Lấy danh sách tất cả người mượn"""
        connection = create_connection()
        if connection is None: return []
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Borrowers ORDER BY BorrowerID ASC"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_all_borrowers: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_borrower(self, name, email, phone):
        """Thêm người mượn mới"""
        connection = create_connection()
        if connection is None: return False
        cursor = connection.cursor()
        try:
            query = "INSERT INTO Borrowers (BorrowerName, Email, Phone) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, phone))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error add_borrower: {err}")
            # Có thể lỗi do trùng Email (nếu Email là UNIQUE trong DB)
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_borrower(self, borrower_id, name, email, phone):
        """Cập nhật thông tin người mượn"""
        connection = create_connection()
        if connection is None: return False
        cursor = connection.cursor()
        try:
            query = """
                UPDATE Borrowers 
                SET BorrowerName = %s, Email = %s, Phone = %s 
                WHERE BorrowerID = %s
            """
            cursor.execute(query, (name, email, phone, borrower_id))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error update_borrower: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_borrower(self, borrower_id):
        """Xóa người mượn"""
        connection = create_connection()
        if connection is None: return False
        cursor = connection.cursor()
        try:
            query = "DELETE FROM Borrowers WHERE BorrowerID = %s"
            cursor.execute(query, (borrower_id,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error delete_borrower: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()