from flask import *
from mysql.connector.pooling import MySQLConnectionPool
from data.dbconfig import user,password
booking=Blueprint('booking',__name__)

db=MySQLConnectionPool(
	host='localhost',
	user=user, 
	password=password, # change config when upload
	database='taipeispot',
	pool_name='my_connection_pool',
	pool_size=10,
	pool_reset_session=True
)

@booking.route('/booking',methods=['GET','POST','DELETE'])
def book():
    json_data={}
    if 'id' in session:
        if request.method=='GET':
            print('get booking')
            print(session)
            if 'data' in session:
                json_data['data']=session['data']
            else:
                json_data['data']=None
            print(json_data)
        
        elif request.method=='POST':
            print('post booking')
            print(request.json)
            if request.json['date']=='' or request.json['price']==None:
                abort(400,'建立失敗')
            try:
                conn=db.get_connection()
                mycursor=conn.cursor()
                mycursor.execute(f'select id,name,address,images from spot where id like {request.json["attractionId"]}')
            except:
                abort(500)
            db_spot=mycursor.fetchone()
            column_name=mycursor.column_names
            conn.close()
            book_data={}
            attraction={}
            for column,info in zip(column_name,db_spot):
                if column=='images':
                    attraction['image']=info.split()[0]
                else:
                    attraction[column]=info
            book_data['attraction']=attraction
            book_data['date']=request.json['date']
            book_data['time']=request.json['time']
            book_data['price']=request.json['price']
            session['data']=book_data
            json_data['ok']=True
        
                
        elif request.method=='DELETE':
            print('delete booking')
            session.pop('data')
            print(session)
            json_data['ok']=True

        else:
            abort(500)
    else:
        abort(403,'未登入系統')
    return jsonify(json_data),200