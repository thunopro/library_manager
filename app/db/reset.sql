USE library_db;

-- 1. Tắt chế độ kiểm tra khóa ngoại (để xóa được bất chấp ràng buộc)
SET FOREIGN_KEY_CHECKS = 0;

-- 2. Làm sạch dữ liệu và reset ID về 1 (TRUNCATE)
TRUNCATE TABLE Loans;
TRUNCATE TABLE Books;
TRUNCATE TABLE Authors;
TRUNCATE TABLE Borrowers;

-- 3. Bật lại chế độ kiểm tra khóa ngoại (để đảm bảo an toàn cho lần sau)
SET FOREIGN_KEY_CHECKS = 1;