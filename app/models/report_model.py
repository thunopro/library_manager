import mysql.connector
from app.db.connection import create_connection

class ReportModel:
    def get_kpis(self):
        """Lấy số liệu tổng quan cho Dashboard"""
        conn = create_connection()
        if conn is None: return {'total_books': 0, 'total_borrowers': 0, 'active_loans': 0, 'overdue_count': 0}
        
        cursor = conn.cursor()
        kpis = {}
        try:
            # 1. Tổng sách
            cursor.execute("SELECT COUNT(*) FROM Books")
            kpis['total_books'] = cursor.fetchone()[0]
            
            # 2. Tổng người mượn
            cursor.execute("SELECT COUNT(*) FROM Borrowers")
            kpis['total_borrowers'] = cursor.fetchone()[0]
            
            # 3. Sách đang mượn (Status = Borrowed hoặc Overdue)
            cursor.execute("SELECT COUNT(*) FROM Loans WHERE Status IN ('Borrowed', 'Overdue')")
            kpis['active_loans'] = cursor.fetchone()[0]
            
            # 4. Sách quá hạn
            cursor.execute("SELECT COUNT(*) FROM Loans WHERE Status = 'Overdue'")
            kpis['overdue_count'] = cursor.fetchone()[0]
        except Exception as e:
            print(f"Lỗi lấy KPI: {e}")
        finally:
            conn.close()
            
        return kpis

    # --- QUERY 1: INNER JOIN (Yêu cầu 2.2.1) ---
    def get_borrowing_activity(self):
        """Lấy danh sách ai đang mượn sách gì (chỉ hiện người có mượn)"""
        conn = create_connection()
        cursor = conn.cursor()
        query = """
            SELECT br.BorrowerName, b.BookTitle, l.Status
            FROM Loans l
            JOIN Borrowers br ON l.BorrowerID = br.BorrowerID
            JOIN Books b ON l.BookID = b.BookID
            ORDER BY l.BorrowedDate DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    # --- QUERY 2: LEFT JOIN (Yêu cầu 2.2.2) ---
    def get_all_borrowers_status(self):
        """Lấy tất cả người mượn, kể cả người CHƯA mượn cuốn nào"""
        conn = create_connection()
        cursor = conn.cursor()
        # Dùng LEFT JOIN từ bảng Borrowers sang Loans
        query = """
            SELECT br.BorrowerName, b.BookTitle, l.Status
            FROM Borrowers br
            LEFT JOIN Loans l ON br.BorrowerID = l.BorrowerID
            LEFT JOIN Books b ON l.BookID = b.BookID
            ORDER BY br.BorrowerName ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    # --- QUERY 3: MULTI-TABLE JOIN (3+ tables) (Yêu cầu 2.2.3) ---
    def get_full_loan_details(self):
        """Lấy chi tiết: Người, Sách, Tác giả (Bảng thứ 3), Ngày Mượn"""
        conn = create_connection()
        cursor = conn.cursor()
        # Join 4 bảng: Loans, Borrowers, Books, Authors
        query = """
            SELECT br.BorrowerName, b.BookTitle, a.AuthorName, l.BorrowedDate, l.DueDate
            FROM Loans l
            JOIN Borrowers br ON l.BorrowerID = br.BorrowerID
            JOIN Books b ON l.BookID = b.BookID
            LEFT JOIN Authors a ON b.AuthorID = a.AuthorID
            ORDER BY l.BorrowedDate DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    # --- QUERY 4: OVERDUE (Yêu cầu 2.2.4 - Bạn đã có) ---
    def get_overdue_report(self):
        """Lấy danh sách sách quá hạn"""
        conn = create_connection()
        cursor = conn.cursor()
        query = """
            SELECT br.BorrowerName, b.BookTitle, l.DueDate, l.Status
            FROM Loans l
            JOIN Borrowers br ON l.BorrowerID = br.BorrowerID
            JOIN Books b ON l.BookID = b.BookID
            WHERE l.Status = 'Overdue'
            ORDER BY l.DueDate ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result