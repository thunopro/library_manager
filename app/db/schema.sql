    -- 1. Tạo Database (nếu chưa có) và sử dụng nó
    CREATE DATABASE IF NOT EXISTS library_db;
    USE library_db;

    -- 2. Xóa các bảng cũ nếu tồn tại (để chạy lại không bị lỗi)
    -- Phải xóa bảng con (Loans, Books) trước bảng cha (Authors, Borrowers)
    DROP TABLE IF EXISTS Loans;
    DROP TABLE IF EXISTS Books;
    DROP TABLE IF EXISTS Authors;
    DROP TABLE IF EXISTS Borrowers;

    -- 3. Tạo bảng Tác giả (Authors) - 3NF tách từ Books
    CREATE TABLE Authors (
        AuthorID INT AUTO_INCREMENT PRIMARY KEY,
        AuthorName VARCHAR(255) NOT NULL
    );

    -- 4. Tạo bảng Sách (Books)
    CREATE TABLE Books (
        BookID INT AUTO_INCREMENT PRIMARY KEY,
        BookTitle VARCHAR(255) NOT NULL,
        AuthorID INT, -- Khóa ngoại trỏ về Authors
        FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE SET NULL
    );

    -- 5. Tạo bảng Người mượn (Borrowers)
    CREATE TABLE Borrowers (
        BorrowerID INT AUTO_INCREMENT PRIMARY KEY,
        BorrowerName VARCHAR(255) NOT NULL,
        Email VARCHAR(255) UNIQUE,
        Phone VARCHAR(20)
    );

    -- 6. Tạo bảng Mượn trả (Loans)
    CREATE TABLE Loans (
        LoanID INT AUTO_INCREMENT PRIMARY KEY,
        BorrowerID INT NOT NULL,
        BookID INT NOT NULL,
        BorrowedDate DATE NOT NULL,
        DueDate DATE NOT NULL,
        Status ENUM('Borrowed', 'Returned', 'Overdue') DEFAULT 'Borrowed',
        FOREIGN KEY (BorrowerID) REFERENCES Borrowers(BorrowerID) ON DELETE CASCADE,
        FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE
    );