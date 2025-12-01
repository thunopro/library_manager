USE library_db;

-- =============================================
-- 1. Thêm Tác giả (Authors) - Yêu cầu: 8-12 (Hiện tại: 12)
-- =============================================
INSERT INTO Authors (AuthorName) VALUES 
('Nguyễn Nhật Ánh'),
('Nam Cao'),
('Tô Hoài'),
('J.K. Rowling'),
('Dan Brown'),
('Agatha Christie'),
('Haruki Murakami'),
('Stephen King'),
('George Orwell'),
('Victor Hugo'),
('Vũ Trọng Phụng'),  -- Mới thêm
('Paulo Coelho');     -- Mới thêm

-- =============================================
-- 2. Thêm Sách (Books) - Yêu cầu: 10-15 (Hiện tại: 15)
-- =============================================
INSERT INTO Books (BookTitle, AuthorID) VALUES 
('Kính Vạn Hoa', 1),
('Cho Tôi Xin Một Vé Đi Tuổi Thơ', 1),
('Chí Phèo', 2),
('Dế Mèn Phiêu Lưu Ký', 3),
('Harry Potter và Hòn Đá Phù Thủy', 4),
('Mật mã Da Vinci', 5),
('Án mạng trên sông Nile', 6),
('Rừng Na Uy', 7),
('It (Gã Hề Ma Quái)', 8),
('1984', 9),
('Những người khốn khổ', 10),
('Nhà Giả Kim', 12),
('Đắc Nhân Tâm', NULL),
('Số Đỏ', 11),                   -- Mới thêm
('Mắt Biếc', 1);                 -- Mới thêm

-- =============================================
-- 3. Thêm Người mượn (Borrowers) - Yêu cầu: >= 10 (Hiện tại: 15)
-- =============================================
INSERT INTO Borrowers (BorrowerName, Email, Phone) VALUES 
('Nguyễn Văn A', 'vana@example.com', '0901234567'),
('Trần Thị B', 'thib@example.com', '0901234568'),
('Lê Văn C', 'vanc@example.com', '0901234569'),
('Phạm Thị D', 'thid@example.com', '0901234570'),
('Hoàng Văn E', 'vane@example.com', '0901234571'),
('Đỗ Thị F', 'thif@example.com', '0901234572'),
('Ngô Văn G', 'vang@example.com', '0901234573'),
('Bùi Thị H', 'thih@example.com', '0901234574'),
('Đặng Văn I', 'vani@example.com', '0901234575'),
('Vũ Thị K', 'thik@example.com', '0901234576'),
('Lý Văn L', 'vanl@example.com', '0901234577'), -- Mới thêm
('Trương Thị M', 'thim@example.com', '0901234578'), -- Mới thêm
('Đinh Văn N', 'vann@example.com', '0901234579'), -- Mới thêm
('Khổng Tú Q', 'tuq@example.com', '0901234580'), -- Mới thêm
('Hồ Văn P', 'vanp@example.com', '0901234581'); -- Mới thêm

-- =============================================
-- 4. Thêm Lượt mượn (Loans) - Yêu cầu: 30-50 (Hiện tại: 43)
-- Logic: 
-- - 'Returned': Lịch sử cũ, có thể nhiều dòng cho 1 cuốn sách.
-- - 'Borrowed'/'Overdue': Trạng thái hiện tại, mỗi cuốn sách chỉ được có tối đa 1 dòng này (nếu chưa trả).
-- =============================================

-- --- NHÓM 1: LỊCH SỬ ĐÃ TRẢ (Returned) - Khoảng 25 dòng ---
INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(1, 1, '2023-01-05', '2023-01-19', 'Returned'),
(2, 1, '2023-02-01', '2023-02-15', 'Returned'),
(3, 2, '2023-03-10', '2023-03-24', 'Returned'),
(4, 2, '2023-04-05', '2023-04-19', 'Returned'),
(5, 3, '2023-01-15', '2023-01-29', 'Returned'),
(6, 4, '2023-05-01', '2023-05-15', 'Returned'),
(7, 5, '2023-06-10', '2023-06-24', 'Returned'),
(8, 5, '2023-07-01', '2023-07-15', 'Returned'),
(9, 6, '2023-02-20', '2023-03-06', 'Returned'),
(10, 7, '2023-03-15', '2023-03-29', 'Returned'),
(11, 8, '2023-04-10', '2023-04-24', 'Returned'),
(12, 9, '2023-05-05', '2023-05-19', 'Returned'),
(13, 10, '2023-06-01', '2023-06-15', 'Returned'),
(14, 11, '2023-07-20', '2023-08-03', 'Returned'),
(15, 12, '2023-08-01', '2023-08-15', 'Returned'),
(1, 13, '2023-08-15', '2023-08-29', 'Returned'),
(2, 14, '2023-09-01', '2023-09-15', 'Returned'),
(3, 15, '2023-09-10', '2023-09-24', 'Returned'),
(4, 3, '2023-02-01', '2023-02-15', 'Returned'),
(5, 4, '2023-06-01', '2023-06-15', 'Returned'),
(6, 1, '2023-03-01', '2023-03-15', 'Returned'), -- Sách 1 được mượn nhiều lần
(7, 2, '2023-05-20', '2023-06-03', 'Returned');

-- --- NHÓM 2: ĐANG MƯỢN (Borrowed) - Những người đang giữ sách ---
-- Lưu ý: BookID ở đây không được trùng với BookID ở Nhóm 3
INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(1, 2, '2023-11-20', '2023-12-05', 'Borrowed'), -- Sách 2 đang được mượn
(3, 5, '2023-11-25', '2023-12-10', 'Borrowed'), -- Sách 5 đang được mượn
(5, 7, '2023-11-28', '2023-12-12', 'Borrowed'),
(6, 9, '2023-11-29', '2023-12-13', 'Borrowed'),
(7, 10, '2023-11-30', '2023-12-14', 'Borrowed'),
(11, 12, '2023-11-15', '2023-11-30', 'Borrowed'),
(12, 13, '2023-11-22', '2023-12-07', 'Borrowed'),
(14, 15, '2023-11-25', '2023-12-09', 'Borrowed');

-- --- NHÓM 3: QUÁ HẠN (Overdue) - Mượn lâu rồi chưa trả ---
-- Logic: BorrowedDate cũ, DueDate < Ngày hiện tại
INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(2, 3, '2023-09-01', '2023-09-15', 'Overdue'),   -- Chí Phèo bị giữ quá hạn
(4, 6, '2023-08-10', '2023-08-25', 'Overdue'),   -- Mật mã Da Vinci quá hạn
(8, 4, '2023-09-05', '2023-09-20', 'Overdue'),   -- Dế Mèn quá hạn
(9, 1, '2023-10-01', '2023-10-15', 'Overdue'),   -- Kính Vạn Hoa quá hạn
(10, 8, '2023-10-05', '2023-10-20', 'Overdue'),  -- Rừng Na Uy quá hạn
(13, 11, '2023-09-20', '2023-10-04', 'Overdue'), -- Những người khốn khổ quá hạn
(15, 14, '2023-09-15', '2023-09-30', 'Overdue'); -- Số Đỏ quá hạn