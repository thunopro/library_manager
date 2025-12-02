USE library_db;

-- =============================================
-- 1. Thêm Tác giả (Authors) - (International Authors)
-- =============================================
INSERT INTO Authors (AuthorName) VALUES 
('J.K. Rowling'),           -- ID: 1
('George Orwell'),          -- ID: 2
('J.R.R. Tolkien'),         -- ID: 3
('Agatha Christie'),        -- ID: 4
('Dan Brown'),              -- ID: 5
('Stephen King'),           -- ID: 6
('Haruki Murakami'),        -- ID: 7
('F. Scott Fitzgerald'),    -- ID: 8
('Jane Austen'),            -- ID: 9
('Mark Twain'),             -- ID: 10
('Ernest Hemingway'),       -- ID: 11
('Paulo Coelho');           -- ID: 12

-- =============================================
-- 2. Thêm Sách (Books) - (English Titles)
-- =============================================
INSERT INTO Books (BookTitle, AuthorID) VALUES 
('Harry Potter and the Sorcerers Stone', 1),   -- BookID: 1
('Harry Potter and the Chamber of Secrets', 1), -- BookID: 2
('1984', 2),                                    -- BookID: 3
('The Hobbit', 3),                              -- BookID: 4
('Murder on the Orient Express', 4),            -- BookID: 5
('The Da Vinci Code', 5),                       -- BookID: 6
('It', 6),                                      -- BookID: 7
('Norwegian Wood', 7),                          -- BookID: 8
('The Great Gatsby', 8),                        -- BookID: 9
('Pride and Prejudice', 9),                     -- BookID: 10
('The Adventures of Tom Sawyer', 10),           -- BookID: 11
('The Alchemist', 12),                          -- BookID: 12
('Beowulf', NULL),                              -- BookID: 13 (Tác giả khuyết danh)
('The Old Man and the Sea', 11),                -- BookID: 14
('Animal Farm', 2);                             -- BookID: 15

-- =============================================
-- 3. Thêm Người mượn (Borrowers) 
-- (Giữ nguyên tên tiếng Việt cho dễ quản lý hoặc bạn có thể đổi nếu thích)
-- =============================================
INSERT INTO Borrowers (BorrowerName, Email, Phone) VALUES 
('Nguyen Van A', 'vana@example.com', '0901234567'),
('Tran Thi B', 'thib@example.com', '0901234568'),
('Le Van C', 'vanc@example.com', '0901234569'),
('Pham Thi D', 'thid@example.com', '0901234570'),
('Hoang Van E', 'vane@example.com', '0901234571'),
('Do Thi F', 'thif@example.com', '0901234572'),
('Ngo Van G', 'vang@example.com', '0901234573'),
('Bui Thi H', 'thih@example.com', '0901234574'),
('Dang Van I', 'vani@example.com', '0901234575'),
('Vu Thi K', 'thik@example.com', '0901234576'),
('Ly Van L', 'vanl@example.com', '0901234577'),
('Truong Thi M', 'thim@example.com', '0901234578'),
('Dinh Van N', 'vann@example.com', '0901234579'),
('Khong Tu Q', 'tuq@example.com', '0901234580'),
('Ho Van P', 'vanp@example.com', '0901234581');

-- =============================================
-- 4. Thêm Lượt mượn (Loans)
-- (Dữ liệu này ánh xạ theo ID của Book và Borrower nên không cần sửa gì nhiều, chỉ cần chạy lại)
-- =============================================

-- --- NHÓM 1: LỊCH SỬ ĐÃ TRẢ (Returned) ---
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
(6, 1, '2023-03-01', '2023-03-15', 'Returned'),
(7, 2, '2023-05-20', '2023-06-03', 'Returned');

-- --- NHÓM 2: ĐANG MƯỢN (Borrowed) ---
INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(1, 2, '2023-11-20', '2023-12-05', 'Borrowed'),
(3, 5, '2023-11-25', '2023-12-10', 'Borrowed'),
(5, 7, '2023-11-28', '2023-12-12', 'Borrowed'),
(6, 9, '2023-11-29', '2023-12-13', 'Borrowed'),
(7, 10, '2023-11-30', '2023-12-14', 'Borrowed'),
(11, 12, '2023-11-15', '2023-11-30', 'Borrowed'),
(12, 13, '2023-11-22', '2023-12-07', 'Borrowed'),
(14, 15, '2023-11-25', '2023-12-09', 'Borrowed');

-- --- NHÓM 3: QUÁ HẠN (Overdue) ---
INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) VALUES 
(2, 3, '2023-09-01', '2023-09-15', 'Overdue'),   -- 1984
(4, 6, '2023-08-10', '2023-08-25', 'Overdue'),   -- The Da Vinci Code
(8, 4, '2023-09-05', '2023-09-20', 'Overdue'),   -- The Hobbit
(9, 1, '2023-10-01', '2023-10-15', 'Overdue'),   -- Harry Potter 1
(10, 8, '2023-10-05', '2023-10-20', 'Overdue'),  -- Norwegian Wood
(13, 11, '2023-09-20', '2023-10-04', 'Overdue'), -- Tom Sawyer
(15, 14, '2023-09-15', '2023-09-30', 'Overdue'); -- The Old Man and the Sea