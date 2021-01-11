CREATE DATABASE project3;
USE project3;

CREATE TABLE Book( 
    ISBN CHAR(13) PRIMARY KEY, 
    Name VARCHAR(50), 
    Page INT, 
    Genres VARCHAR(255),
    Author VARCHAR(50) );

CREATE TABLE filteredBooks( 
    ISBN CHAR(13) PRIMARY KEY, 
    Name VARCHAR(50), 
    Page INT, 
    Genres VARCHAR(255),
    Author VARCHAR(50) );

CREATE TABLE Borrower( 
    TC_Num CHAR(11) PRIMARY KEY, 
    Full_Name VARCHAR(50), 
    Book_Num INT );

CREATE TABLE BorrowBook( 
    TC_Num CHAR(11), 
    ISBN CHAR(13), 
    Duedate DATE,
    PRIMARY KEY (TC_Num, ISBN) );

delimiter //

-- SELECT student-name FROM STUDENT WHERE NOT EXISTS(
--     SELECT * FROM BOOK WHERE NOT EXISTS(
--         SELECT * FROM READ-BOOK WHERE READ-BOOK.book-id BOOK.book-id AND BOOK.author-name = AUTHOR.author-name AND AUTHOR.age > 50 AND READ-BOOK.student-id = STUDENT.student-id    
--     ) 
-- )

-- SELECT student-name FROM STUDENT WHERE NOT EXISTS(
--     SELECT * FROM BOOK WHERE NOT EXISTS(
--         SELECT * FROM READ-BOOK WHERE READ-BOOK.book-id in (
--             SELECT BOOK.book-id FROM BOOK WHERE BOOK.author-name in (
--                 SELECT AUTHOR.author-name FROM AUTHOR WHERE AUTHOR.age > 50 
--             )
--         )    
--     ) 
-- )

-- SELECT STUDENT.student-name 
-- FROM STUDENT
-- WHERE STUDENT.student-id in (
--     SELECT READ-BOOK.student-id
--     FROM READ-BOOK
--     WHERE READ-BOOK.book-id in (
--         SELECT BOOK.book-id
--         FROM BOOK 
--         WHERE BOOK.author-name in (
--             SELECT AUTHOR.author-name
--             FROM AUTHOR
--             WHERE AUTHOR.age > 50 
--         )
--     )      
-- )


CREATE FUNCTION deleteBook(target VARCHAR(13)) RETURNS BOOLEAN
    BEGIN
        IF NOT EXISTS(
            SELECT * FROM Book WHERE ISBN = target)
        THEN RETURN FALSE;
        ELSE
            DELETE FROM Book WHERE ISBN = target;
            UPDATE Borrower SET Book_Num = Book_Num-1 WH    ERE TC_Num=(SELECT TC_Num FROM BorrowBook WHERE ISBN = target);
            DELETE FROM BorrowBook WHERE ISBN = target;
            RETURN TRUE;
        END IF;
    END//

CREATE FUNCTION filterGenre(Genrei VARCHAR(255)) RETURNS BOOLEAN
    BEGIN
        IF Genrei <> " "
        THEN DELETE FROM filteredBooks where Genres NOT LIKE Genrei; RETURN TRUE; 
        ELSE
            RETURN FALSE;
        END IF;
    END//

CREATE FUNCTION availableBooks() RETURNS BOOLEAN
    BEGIN
        DELETE FROM filteredBooks;
        INSERT INTO filteredBooks SELECT * FROM Book;
        DELETE FROM filteredBooks WHERE ISBN IN(SELECT ISBN FROM BorrowBook) ; 
        RETURN TRUE;
    END//

CREATE PROCEDURE searchBook (IN ISBNi VARCHAR(255),IN Namei VARCHAR(50),IN PageMini INT,IN PageMaxi INT,IN Authori VARCHAR(50))
    BEGIN
        DELETE FROM filteredBooks;
        INSERT INTO filteredBooks SELECT * FROM Book;

        IF ISBNi <> " " 
        THEN DELETE FROM filteredBooks WHERE ISBN <> ISBNi; 
        ELSEIF Namei <> " "
        THEN DELETE FROM filteredBooks WHERE Name NOT LIKE Namei ; 
        ELSEIF PageMini <> -1
        THEN DELETE FROM filteredBooks WHERE Page < PageMini; 
        ELSEIF PageMaxi <> -1
        THEN DELETE FROM filteredBooks WHERE Page > PageMaxi; 
        ELSEIF Authori <> " "
        THEN DELETE FROM filteredBooks WHERE Author NOT LIKE Authori ; 
           
        END IF;
    END//

CREATE TRIGGER dateAssign BEFORE INSERT ON BorrowBook
    FOR EACH ROW
    BEGIN
        SET NEW.Duedate =  (SELECT CURDATE() + 14);
    END//

CREATE FUNCTION borrowBook(tc_numi VARCHAR(255), ISBNi VARCHAR(255)) RETURNS INT
    BEGIN
        IF NOT EXISTS(
            SELECT * FROM Borrower WHERE TC_Num = tc_numi)
        THEN RETURN 2;

        ELSEIF NOT EXISTS(
             SELECT * FROM Book WHERE ISBN = ISBNi)
        THEN RETURN 3;

        ELSEIF EXISTS(
             SELECT * FROM BorrowBook WHERE ISBN = ISBNi )
        THEN RETURN 4;
        ELSEIF 8 = (SELECT Book_Num FROM Borrower WHERE TC_Num = tc_numi)
        THEN RETURN 5;
        ELSE
            INSERT INTO BorrowBook(TC_Num,ISBN) VALUES(tc_numi,ISBNi);
            UPDATE Borrower SET Book_Num = Book_Num+1 WHERE TC_Num = tc_numi;
            RETURN 1;
        END IF;
    END//

CREATE FUNCTION returnBook(ISBNi VARCHAR(255)) RETURNS INT
    BEGIN
        IF NOT EXISTS(
             SELECT * FROM Book WHERE ISBN = ISBNi)
        THEN RETURN 2;

        ELSEIF NOT EXISTS(
             SELECT * FROM BorrowBook WHERE ISBN = ISBNi )
        THEN RETURN 3;
        ELSE
            UPDATE Borrower SET Book_Num = Book_Num-1 WHERE TC_Num=(SELECT TC_Num FROM BorrowBook WHERE ISBN = ISBNi);
            DELETE FROM BorrowBook WHERE ISBN = ISBNi;
            RETURN 1;
        END IF;
    END//
delimiter ;





