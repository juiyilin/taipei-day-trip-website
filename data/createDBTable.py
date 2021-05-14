import mysql.connector 
from dbconfig import user,password

def createDB(cursor,DBname):
    try:
        cursor.execute(f"create database {DBname}")
        
    except mysql.connector.errors.DatabaseError:
        print('already exist',DBname)
    else:
        print(DBname+' created')   

db = mysql.connector.connect(
    host="localhost",
    user=user,
    password=password
)
mycursor = db.cursor()

# database taipeispot
createDB(mycursor,'taipeispot')
db.database='taipeispot'
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

# database users
createDB(mycursor,'users')
db.database='users'
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