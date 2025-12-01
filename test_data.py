from app.db.connection import create_connection

def test_get_books():
    # 1. Mở kết nối
    conn = create_connection()
    
    if conn:
        cursor = conn.cursor(dictionary=True) # dictionary=True để kết quả trả về dạng từ điển {'TenCot': 'GiaTri'}
        
        # 2. Thực hiện câu query lấy sách + tên tác giả
        query = """
        SELECT b.BookTitle, a.AuthorName, b.BookID
        FROM Books b
        LEFT JOIN Authors a ON b.AuthorID = a.AuthorID
        LIMIT 5;
        """
        
        cursor.execute(query)
        books = cursor.fetchall()
        
        # 3. In kết quả ra màn hình
        print(f"\n{'ID':<5} | {'Tên Sách':<40} | {'Tác Giả'}")
        print("-" * 70)
        for book in books:
            # Xử lý trường hợp tác giả là None
            author = book['AuthorName'] if book['AuthorName'] else "Chưa rõ"
            print(f"{book['BookID']:<5} | {book['BookTitle']:<40} | {author}")
            
        # 4. Đóng kết nối
        cursor.close()
        conn.close()
    else:
        print("Không thể kết nối CSDL")

if __name__ == "__main__":
    test_get_books()