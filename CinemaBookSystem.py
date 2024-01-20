from graphics import *
import time
import copy
import random
import mysql.connector as sqltor

def main():
    print("Welcome to the Cinema Seat Booking System")
    Options()

def create_window():
    global win
    win = GraphWin('Cinema Seat Booking System',1000,600)
    Text(Point(23.5,30),"MOVIE SCREEN").draw(win)
    
def create_graphics_for_seats():
    create_window()
    win.setCoords(0.0,0.0,50.0,40.0)
    Point1_xCoord = 0.5
    Point1_yCoord = 0.5
    Point2_xCoord = 2.5
    Point2_yCoord = 2.5

    List_of_Coordinates = []
    rows_list = []

    Row = "ABCDEFGHIJ"
    for j in range(10):
        
        rows_list=[]
        
        for i in range(20):
            seat = Rectangle(Point(Point1_xCoord,Point1_yCoord),Point(Point2_xCoord,Point2_yCoord))

            L = [Point1_xCoord,Point2_yCoord]
            rows_list.append(L)
            
            Point1_xCoord = Point1_xCoord + 2.25
            Point2_xCoord = Point2_xCoord + 2.25
            if (j >= 2 and i < 2) or (j >= 2 and i > 17):
                pass
            else:
                seat.draw(win)
                if j < 2 :
                    seat.setFill("orange")

        Text(Point(Point2_xCoord - 0.5 ,Point2_yCoord - 1.0),Row[j]).draw(win)
        
        Point1_xCoord = 0.5
        Point2_xCoord = 2.5
        Point1_yCoord = Point1_yCoord + 2.5
        Point2_yCoord = Point2_yCoord + 2.5

        List_of_Coordinates.append(rows_list)

    return List_of_Coordinates

def Book_Tickets(List_of_Coordinates,movie_name):
    customer_id = random.randint(1,1000)
    customer_name = input(" Please Enter the name of the customer- ")
    num = int(input("How many seats do you want to book? "))
    print("Please select the seat(s) - ")
    for i in range(num):
        
        click = win.getMouse()
        X_coordinate = click.getX()
        Y_coordinate = click.getY()
        
        for j in List_of_Coordinates:
            for k in j:
                xcoordinate_check = k[0]
                ycoordinate_check = k[1]

                if (xcoordinate_check < X_coordinate and X_coordinate < xcoordinate_check  +  2) and (ycoordinate_check - 2  < Y_coordinate and Y_coordinate < ycoordinate_check):
                    change_seat = Rectangle(Point(xcoordinate_check,ycoordinate_check),Point(xcoordinate_check + 2 ,ycoordinate_check - 2))
                    change_seat.setFill('red')
                    change_seat.draw(win)

    connectivity_with_SQL(customer_id,customer_name,movie_name,num)
                    
    return Options()

def DeleteBookedTickets(List_of_Coordinates):
    num = int(input("How many seats do you want to delete? "))
    print("Please select the seat(s) - ")
    for i in range(num):
        
        click = win.getMouse()
        X_coordinate = click.getX()
        Y_coordinate = click.getY()
        
        for j in List_of_Coordinates:
            for k in j:
                xcoordinate_check = k[0]
                ycoordinate_check = k[1]
                        
                if (xcoordinate_check < X_coordinate and X_coordinate < xcoordinate_check  +  2) and (ycoordinate_check - 2  < Y_coordinate and Y_coordinate < ycoordinate_check):
                    change_seat = Rectangle(Point(xcoordinate_check,ycoordinate_check),Point(xcoordinate_check + 2 ,ycoordinate_check - 2))
                    change_seat.setFill('white')
                    change_seat.draw(win)
                

    return Options()

def QuitWindow():
    win.close()
    
 
def Options():
    print("Which of the following operations do you want to perform - \
    \n 1. Booking tickets for a Movie \
    \n 2. Deleting Booked tickets \
    \n 3. Quit ")
    opt = int(input("Enter the option number - "))
    
    
    if opt == 1:
        moname = Ask_Movie()
        Book_Tickets(x,moname)
        
    elif opt == 2:
        DeleteBookedTickets(x)
    elif opt == 3:
        QuitWindow()
    else:
        print("Error! Enter correct option!")
        return Options()

x = copy.copy(create_graphics_for_seats())


def Ask_Movie():
    print("Movie Theatre")
    print("-------------")
    print("1 --> John Wick 3")
    print("2 --> Batman")
    print("3 --> Tenet")
    MovieNo = int(input("Enter the Movie Number - "))
    if MovieNo == 1:
        Text(Point(23.5,35),"John Wick 3").draw(win)
        return "John Wick 3"
    elif MovieNo == 2:
        Text(Point(23.5,35),"Batman").draw(win)
        return "Batman"
    elif MovieNo == 3:
        Text(Point(23.5,35),"Tenet").draw(win)
        return "Tenet"
    else:
        print("Error!")
        Ask_Movie()


def checkTableExists(dbcursor, tablename):
    
    dbcursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'".format(tablename.replace('\'', '\'\'')))
    if dbcursor.fetchone()[0] == 1:
        return True
    return False

def connectivity_with_SQL(customer_id,customer_name,movie_name,number_of_seats):
    config = {
        "user": "root",
        "password": "redwedred",
        "host": "localhost",
    }
    
    c = sqltor.connect(**config)
        
    mycursor = c.cursor(buffered=True)
    
    mycursor.execute("create database if not exists movies")
    mycursor.execute("use movies")

    if checkTableExists(mycursor, "movie1") == False:
        mycursor.execute("create table movie1(customer_id varchar(10) primary key, name varchar(32), movie_name varchar(32), seats varchar(32))")
        mycursor.execute("create table movie2(customer_id varchar(10) primary key, name varchar(32), movie_name varchar(32), seats varchar(32))")
        mycursor.execute("create table movie3(customer_id varchar(10) primary key, name varchar(32), movie_name varchar(32), seats varchar(32))")
    else:
        pass
    print(movie_name)
    if movie_name == "John Wick 3":
        mycursor.execute("insert into movie1 values(%s,%s,%s,%s)",(customer_id, customer_name, movie_name, number_of_seats))
        c.commit()
    elif movie_name == "Batman":
        mycursor.execute("insert into movie2 values(%s,%s,%s,%s)",(customer_id, customer_name, movie_name, number_of_seats))
        c.commit()
    else:
        mycursor.execute("insert into movie3 values(%s,%s,%s,%s)",(customer_id, customer_name, movie_name, number_of_seats))
        c.commit()
    
main()
