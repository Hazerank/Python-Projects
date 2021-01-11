from flask import render_template, request, redirect
from app import app
from flask_mysqldb import MySQL

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')

@app.route('/createBook', methods=['GET','POST'])
def createBook():
    try:
        details = request.form
        isbn = details['ISBN']
        name = details['Name']
        page = details['Page']
        genres = details['Genres']
        author = details['Author']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Book VALUES('%s', '%s', %s, '%s', '%s');" % (isbn, name,page,genres,author))
        mysql.connection.commit()
        cur.close()
        return render_template('createBook.html')
    except Exception as e:
        print(e)
        if "Duplicate entry" in str(e):
            return render_template('createBook.html',error="ISBN values should be unique, there is already a book in the system with this ISBN")
        return render_template('createBook.html',error=e)

@app.route('/deleteBook', methods=['GET','POST'])
def deleteBook():
    try:
        details = request.form
        isbn = details['ISBN']
        cur = mysql.connection.cursor()
        cur.execute("SELECT deleteBook('%s');" % (isbn))
        mysql.connection.commit()
        value= cur.fetchone()[0]
        if value == 0:
            cur.close()
            return render_template('deleteBook.html',error="There is no book with ISBN value: '" + isbn+ "'")
        else:
            cur.close()
            return render_template('deleteBook.html')    
    except Exception as e:
        print(e)
        return render_template('deleteBook.html',error=e) 

@app.route('/searchBook', methods=['GET','POST'])
def searchBook():
    try:
        details = request.form
        info = []
        free = True
        isbn = details['ISBN']
        if isbn != "":
            free = False
            info.append("ISBN: " + isbn)
        else:
            isbn = " "
        name = details['Name']
        if name != "":
            free = False
            info.append(" Name: " + name)
            name = '%' + name + '%'
        else:
            name = " "

        page_Min = details['Page_Min']
        if page_Min == "":
            page_Min = "-1"
        else:
            free = False
            info.append(" Page min: " + page_Min)

        page_Max = details['Page_Max']
        if page_Max == "":
            page_Max = "-1"
        else:
            free = False
            info.append(" Page max: " + page_Max)
                
        genres = details['Genres']
        if genres != "":
            free = False
            genreList = genres.split(",")
            info.append(" Genres: " + genres)
        else:
            genreList = []
        author = details['Author']
        if author != "":
            free = False
            info.append(" Author: " + author)
            author = '%'+ author + '%'
        else:
            author = " "

        cur = mysql.connection.cursor()
        
        cur.execute("CALL searchBook('%s','%s',%s,%s,'%s');" % (isbn,name,page_Min,page_Max,author))
        for genre in genreList:
            cur.execute("SELECT filterGenre('%s');" % ('%'+ genre + '%'))
        
        cur.execute("SELECT * FROM filteredBooks;")
        result = cur.fetchall() 
        mysql.connection.commit()
        cur.close()
        if result == ():
            return render_template('searchBook.html', info=info, free=free,values=result,empty=True) 
        else: 
            return render_template('searchBook.html',  info=info, free=free,values=result)    
    except Exception as e:
        print(e)
        return render_template('searchBook.html', info=info ,free=free, values=result, error=e) 

@app.route('/borrowBook', methods=['GET','POST'])
def borrowBook():
    try:
        details = request.form
        isbn = details['ISBN']
        tc_Num = details['TC_Num']
        cur = mysql.connection.cursor()
        cur.execute("Select borrowBook(%s, %s);" % (tc_Num,isbn))
        value= cur.fetchone()[0]
        mysql.connection.commit()
        if value == 2:
            return render_template('borrowBook.html', error="TC num is Not registered to the system, please register first !")
        if value == 3:
            return render_template('borrowBook.html', error="Book ISBN is Not registered to the system, please choose a Valid Book !")
        if value == 4:
            return render_template('borrowBook.html', error="This book is already taken by a User, please try again later or with another book  !")
        if value == 5:
            return render_template('borrowBook.html', error="User has 8 book and can't take any more book, please return book before !")  
        cur.close()
        return render_template('borrowBook.html')    
    except Exception as e:
        print(e)
        return render_template('borrowBook.html',error=e) 

@app.route('/returnBook', methods=['GET','POST'])
def returnBook():
    try:
        details = request.form
        isbn = details['ISBN']
        cur = mysql.connection.cursor()
        cur.execute("Select returnBook(%s);" % (isbn))
        value= cur.fetchone()[0]
        mysql.connection.commit()
        if value == 2:
            return render_template('returnBook.html', error=" This book is not in our System, so you can't return it !")
        if value == 3:
            return render_template('returnBook.html', error="This book is not borrowed, already in the library, so you can't return it !")
        cur.close()
        return render_template('returnBook.html')    
    except Exception as e:
        print(e)
        return render_template('returnBook.html',error=e) 

@app.route('/borrowerControl', methods=['GET','POST'])
def borrowerControl():
    try:
        details = request.form
        tc_Num = details['TC_Num']
        cur = mysql.connection.cursor()
        res1 = cur.execute("SELECT Book_Num,Full_Name FROM Borrower WHERE TC_Num = %s" % tc_Num )
        if res1 > 0:
            info = cur.fetchone()
            res2 = cur.execute("SELECT BorrowBook.ISBN,Book.Name,BorrowBook.Duedate FROM BorrowBook,Book,Borrower WHERE BorrowBook.TC_Num = '%s' AND Borrower.TC_Num = '%s' AND BorrowBook.ISBN = Book.ISBN;" % (tc_Num,tc_Num))
            if res2 > 0:
                result = cur.fetchall()
                cur.close()

                return render_template('borrowerControl.html', values=result,info=info)    

            else:
                cur.close()
                return render_template('borrowerControl.html', error="There is no book that you are reading")    
        else:
            cur.close()
            return render_template('borrowerControl.html', error="There is no user with TC num '"+ tc_Num+"' , please register first !")
    except Exception as e:
        print(e)
        return render_template('borrowerControl.html', error=e)   

@app.route('/register', methods=['GET','POST'])
def register():
    try:
        details = request.form
        name = details['Name']
        tc_Num = details['TC_Num']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Borrower VALUES(%s, \'%s\', 0);" % (tc_Num,name))
        mysql.connection.commit()
        cur.close()
        return render_template('register.html')     
    except Exception as e:
        print(e)
        if "Duplicate entry" in str(e):
             return render_template('register.html', error="TC_Num should be unique, there is already a user with that TC_Num") 
        return render_template('register.html', error=e) 

@app.route('/listUsers', methods=['GET','POST'])
def listUsers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Borrower;")
        result = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if result == ():  
            return render_template('listUsers.html',values=result,error="There is no user in the system.")     

        return render_template('listUsers.html',values=result)     
    except Exception as e:
        print(e)
        return render_template('listUsers.html', error=e) 

@app.route('/listAllBooks', methods=['GET','POST'])
def listAllBooks():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Book;")
        result = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if result == ():  
            return render_template('listAllBooks.html',values=result,error="There is no Book in the system.")     

        return render_template('listAllBooks.html',values=result)     
    except Exception as e:
        print(e)
        return render_template('listAllBooks.html', error=e) 

@app.route('/listAvailableBooks', methods=['GET','POST'])
def listAvailableBooks():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT availableBooks()")
        cur.execute("SELECT * FROM filteredBooks;")
        result = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if result == ():  
            return render_template('listAvailableBooks.html',values=result,error="There is no Available Book in the system.")     

        return render_template('listAvailableBooks.html',values=result)     
    except Exception as e:
        print(e)
        return render_template('listAvailableBooks.html', error=e) 

