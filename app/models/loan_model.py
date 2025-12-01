import mysql.connector
from datetime import datetime, timedelta
from app.db.connection import create_connection

class LoanModel:
    def get_all_loans(self):
        """Lấy danh sách lịch sử mượn trả (Kèm tên người và tên sách)"""
        conn = create_connection()
        if conn is None: return []
        cursor = conn.cursor(dictionary=True)
        try:
            # Join 3 bảng để lấy tên thay vì chỉ lấy ID
            query = """
                SELECT l.LoanID, br.BorrowerName, b.BookTitle, 
                       l.BorrowedDate, l.DueDate, l.Status
                FROM Loans l
                JOIN Borrowers br ON l.BorrowerID = br.BorrowerID
                JOIN Books b ON l.BookID = b.BookID
                ORDER BY l.LoanID DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_loans: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def borrow_book(self, borrower_id, book_id):
        """Mượn sách: Thêm dòng mới vào bảng Loans"""
        conn = create_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            # 1. Tính ngày mượn (Hôm nay) và Hạn trả (14 ngày sau)
            borrow_date = datetime.now().strftime('%Y-%m-%d')
            due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            
            # 2. Insert vào DB
            query = """
                INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status)
                VALUES (%s, %s, %s, %s, 'Borrowed')
            """
            cursor.execute(query, (borrower_id, book_id, borrow_date, due_date))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error borrow_book: {err}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def return_book(self, loan_id):
        """Trả sách: Cập nhật Status thành 'Returned'"""
        conn = create_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            query = "UPDATE Loans SET Status = 'Returned' WHERE LoanID = %s"
            cursor.execute(query, (loan_id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error return_book: {err}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_available_books(self):
        """Lấy danh sách sách ĐANG CÓ SẴN (chưa bị mượn)"""
        conn = create_connection()
        if conn is None: return []
        cursor = conn.cursor(dictionary=True)
        try:
            # Logic: Lấy tất cả sách TRỪ ĐI những cuốn đang có trong bảng Loans với status 'Borrowed' hoặc 'Overdue'
            query = """
                SELECT BookID, BookTitle FROM Books
                WHERE BookID NOT IN (
                    SELECT BookID FROM Loans WHERE Status IN ('Borrowed', 'Overdue')
                )
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error available_books: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()