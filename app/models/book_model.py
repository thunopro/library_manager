import mysql.connector
from app.db.connection import create_connection

class BookModel:
    def get_all_books(self):
        """Lấy danh sách sách kèm trạng thái"""
        connection = create_connection()
        if connection is None: return []
        cursor = connection.cursor(dictionary=True)
        # Query lấy sách và trạng thái mượn
        query = """
            SELECT b.BookID, b.BookTitle, b.AuthorID, a.AuthorName,
            (SELECT Status FROM Loans l WHERE l.BookID = b.BookID AND l.Status IN ('Borrowed', 'Overdue') LIMIT 1) as CurrentStatus
            FROM Books b
            LEFT JOIN Authors a ON b.AuthorID = a.AuthorID
            ORDER BY b.BookID ASC;
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_all: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # --- CÁC HÀM QUAN TRỌNG CHO POPUP (Bạn đang thiếu phần này) ---
    
    def get_authors(self):
        """Lấy danh sách tác giả để nạp vào Combobox"""
        connection = create_connection()
        if connection is None: return []
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT AuthorID, AuthorName FROM Authors")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_authors: {err}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_book(self, title, author_id):
        """Thêm sách mới"""
        connection = create_connection()
        if connection is None: return False
        cursor = connection.cursor()
        try:
            # Nếu author_id là None (không chọn tác giả), cần xử lý để tránh lỗi SQL
            # Tuy nhiên code main.py hiện tại đã bắt buộc chọn.
            query = "INSERT INTO Books (BookTitle, AuthorID) VALUES (%s, %s)"
            cursor.execute(query, (title, author_id))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error add_book: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    def add_author(self, author_name):
        """Thêm tác giả mới và trả về ID vừa tạo"""
        connection = create_connection()
        if connection is None: return None
        cursor = connection.cursor()
        try:
            # Thêm tác giả mới
            query = "INSERT INTO Authors (AuthorName) VALUES (%s)"
            cursor.execute(query, (author_name,))
            connection.commit()
            
            # Lấy ID của dòng vừa thêm (lastrowid) để dùng cho bảng Books
            new_author_id = cursor.lastrowid 
            return new_author_id
        except mysql.connector.Error as err:
            print(f"Error add_author: {err}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    def update_book(self, book_id, title, author_id):
        """Cập nhật thông tin sách"""
        connection = create_connection()
        if connection is None: return False
        cursor = connection.cursor()
        try:
            query = "UPDATE Books SET BookTitle = %s, AuthorID = %s WHERE BookID = %s"
            cursor.execute(query, (title, author_id, book_id))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error update_book: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_book(self, book_id):
        """Xóa sách"""
        connection = create_connection()
        if connection is None: return False
        cursor = connection.cursor()
        try:
            query = "DELETE FROM Books WHERE BookID = %s"
            cursor.execute(query, (book_id,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error delete_book: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()