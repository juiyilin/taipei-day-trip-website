from mysql.connector.pooling import MySQLConnectionPool
from config import user,password

def db_connect():
	conn=db.get_connection()
	mycursor=conn.cursor()
	return conn,mycursor

def db_close(conn,cursor):
    conn.close()
    cursor.close()


db=MySQLConnectionPool(
	host='localhost',
	user=user, 
	password=password, 
	database='taipeispot',
	pool_name='my_connection_pool',
	pool_size=5,
	pool_reset_session=True
)