import mysql.connector 
import sys
sys.path.append(r"C:\Users\arthu\Desktop\j2\engineer_project\homework\section2\taipei_travel\taipei-day-trip-website")
from config import user,password
print(*sys.path,sep='\n')
def createDB(cursor,DBname):
    try:
        cursor.execute(f"create database {DBname}")
        
    except mysql.connector.errors.DatabaseError:
        print('already exist db',DBname)
    else:
        print(DBname+' created')   

if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database='taipeispot'
    )
    mycursor = db.cursor()

    # database taipeispot
    createDB(mycursor,'taipeispot')
    # table spot
    try:
        mycursor.execute("""CREATE TABLE spot (
            id bigint PRIMARY KEY,
            name VARCHAR(255) CHARACTER SET utf8mb4, 
            category VARCHAR(255) CHARACTER SET utf8mb4, 
            description TEXT CHARACTER SET utf8mb4,
            address VARCHAR(255) CHARACTER SET utf8mb4,
            transport TEXT CHARACTER SET utf8mb4,
            mrt VARCHAR(255) CHARACTER SET utf8mb4,
            latitude VARCHAR(25),
            longitude VARCHAR(25),
            images TEXT)""")
    except mysql.connector.errors.ProgrammingError:
        print('table "spot" exist')
    else:
        print('table "spot" created')


    # table user
    try:
        mycursor.execute("""CREATE TABLE user (
            id bigint PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) CHARACTER SET utf8mb4 NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL)""")
    except mysql.connector.errors.ProgrammingError:
        print('table "user" exist')
    else:
        print('table "user" created')

    # table order
    try:
        mycursor.execute("""CREATE TABLE orders (
            number VARCHAR(255) PRIMARY KEY NOT NULL,
            user_id bigint NOT NULL,
            trip_order TEXT CHARACTER SET utf8mb4 NOT NULL,
            status bigint NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id))""")
    except mysql.connector.errors.ProgrammingError:
        print('table "order" exist')
    else:
        print('table "order" created')

