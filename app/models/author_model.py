# app/models/author_model.py
import mysql.connector
from app.db.connection import create_connection 
# Lưu ý: 'app.db.connection' phải trỏ đúng file kết nối DB của bạn

class AuthorModel:
    def get_all_authors(self):
        """Lấy danh sách tất cả tác giả"""
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Authors ORDER BY AuthorName ASC")
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def add_author(self, name):
        """Thêm tác giả mới"""
        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO Authors (AuthorName) VALUES (%s)"
            cursor.execute(query, (name,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi thêm tác giả: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_author(self, author_id):
        """Xóa tác giả"""
        conn = create_connection()
        cursor = conn.cursor()
        try:
            # Vì trong schema.sql bạn để: ON DELETE SET NULL cho bảng Books
            # Nên khi xóa tác giả, sách của họ sẽ có AuthorID = NULL (vẫn giữ được sách)
            query = "DELETE FROM Authors WHERE AuthorID = %s"
            cursor.execute(query, (author_id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi xóa tác giả: {err}")
            return False
        finally:
            cursor.close()
            conn.close()