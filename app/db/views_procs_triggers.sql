USE library_db;

-- ==========================================
-- VIEWS
-- ==========================================

-- 1) View: Book status with category
CREATE OR REPLACE VIEW v_books_status AS
SELECT
    b.book_id,
    b.title,
    c.category_name,
    b.total_copies,
    b.available_copies
FROM Book b
JOIN Category c ON b.category_id = c.category_id;

-- 2) View: Active loans (Borrowed + Overdue)
CREATE OR REPLACE VIEW v_active_loans AS
SELECT
    l.loan_id,
    m.full_name AS member_name,
    b.title     AS book_title,
    l.issue_date,
    l.due_date,
    l.status
FROM Loan l
JOIN Member m ON l.member_id = m.member_id
JOIN Book   b ON l.book_id   = b.book_id
WHERE l.status IN ('Borrowed','Overdue');

-- 3) View: Overdue fines (theoretical fine based on days overdue)
CREATE OR REPLACE VIEW v_overdue_fines AS
SELECT
    m.member_id,
    m.full_name AS member_name,
    b.title     AS book_title,
    l.due_date,
    GREATEST(DATEDIFF(COALESCE(l.return_date, CURDATE()), l.due_date), 0) AS days_overdue,
    GREATEST(DATEDIFF(COALESCE(l.return_date, CURDATE()), l.due_date), 0) * 10000 AS fine_amount,
    CASE
        WHEN p.payment_id IS NULL THEN 'Unpaid'
        ELSE 'Paid'
    END AS payment_status
FROM Loan l
JOIN Member m ON l.member_id = m.member_id
JOIN Book   b ON l.book_id   = b.book_id
LEFT JOIN Payment p ON l.loan_id = p.loan_id
WHERE l.status = 'Overdue';

-- ==========================================
-- STORED PROCEDURES
-- ==========================================
DELIMITER $$

-- sp_borrow_book: create a new loan and decrease available_copies
CREATE OR REPLACE PROCEDURE sp_borrow_book (
    IN p_member_id INT,
    IN p_book_id   INT
)
BEGIN
    DECLARE v_available INT;

    SELECT available_copies INTO v_available
    FROM Book
    WHERE book_id = p_book_id;

    IF v_available IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Book not found';
    ELSEIF v_available <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No available copies for this book';
    ELSE
        INSERT INTO Loan (member_id, book_id, issue_date, due_date, status)
        VALUES (p_member_id, p_book_id, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'Borrowed');

        UPDATE Book
        SET available_copies = available_copies - 1
        WHERE book_id = p_book_id;
    END IF;
END$$

-- sp_monthly_activity_report: simple monthly summary
CREATE OR REPLACE PROCEDURE sp_monthly_activity_report (
    IN p_year  INT,
    IN p_month INT
)
BEGIN
    SELECT
        p_year  AS year,
        p_month AS month,
        -- number of loans issued in the month
        (SELECT COUNT(*)
         FROM Loan
         WHERE YEAR(issue_date) = p_year
           AND MONTH(issue_date) = p_month) AS loans_issued,
        -- number of returns in the month
        (SELECT COUNT(*)
         FROM Loan
         WHERE status = 'Returned'
           AND return_date IS NOT NULL
           AND YEAR(return_date) = p_year
           AND MONTH(return_date) = p_month) AS loans_returned,
        -- number of overdue loans whose due_date falls in the month
        (SELECT COUNT(*)
         FROM Loan
         WHERE status = 'Overdue'
           AND YEAR(due_date) = p_year
           AND MONTH(due_date) = p_month) AS loans_overdue,
        -- total fines collected in the month
        (SELECT COALESCE(SUM(amount), 0)
         FROM Payment
         WHERE YEAR(payment_date) = p_year
           AND MONTH(payment_date) = p_month) AS total_fines_collected;
END$$

-- ==========================================
-- TRIGGERS
-- ==========================================

-- After UPDATE on Loan: when status changes to Returned, increase available_copies
-- and automatically create a Payment if the book is returned late.
CREATE OR REPLACE TRIGGER trg_loan_after_update
AFTER UPDATE ON Loan
FOR EACH ROW
BEGIN
    DECLARE v_days_overdue INT;
    DECLARE v_amount       DECIMAL(10,2);
    DECLARE v_count        INT;

    -- Only act when going from Borrowed/Overdue -> Returned
    IF OLD.status IN ('Borrowed','Overdue') AND NEW.status = 'Returned' THEN
        -- Increase available copies
        UPDATE Book
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;

        -- If returned late, compute fine and insert Payment if not already exists
        IF NEW.return_date IS NOT NULL AND NEW.return_date > NEW.due_date THEN
            SET v_days_overdue = DATEDIFF(NEW.return_date, NEW.due_date);
            SET v_amount       = v_days_overdue * 10000;

            SELECT COUNT(*) INTO v_count
            FROM Payment
            WHERE loan_id = NEW.loan_id;

            IF v_count = 0 THEN
                INSERT INTO Payment (member_id, loan_id, amount, payment_date, payment_method, remarks)
                VALUES (NEW.member_id, NEW.loan_id, v_amount, NEW.return_date, 'Cash', 'Auto fine for overdue return');
            END IF;
        END IF;
    END IF;
END$$

DELIMITER ;
