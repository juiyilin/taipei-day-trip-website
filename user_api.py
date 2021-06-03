from flask import *
from mysql.connector.pooling import MySQLConnectionPool
from config import user,password

user_account=Blueprint('user',__name__)

db=MySQLConnectionPool(
	host='localhost',
	user=user, 
	password=password, 
	database='taipeispot',
	pool_name='my_connection_pool',
	pool_size=15,
	pool_reset_session=True
)
select_user='select * from user'
@user_account.route('/user', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def check_user():
    json_data={}
    session_keys=['id','name','email']
    if request.method=='GET':
        print('get user')
        if 'id' in session:
            print(session)
            json_data['data']=dict(session)
        else:
            print(session)
            json_data['data']=None
        
    elif request.method=='POST':
        print('post user')
        conn=db.get_connection()
        mycursor=conn.cursor()
        name=request.json['name']
        email=request.json['email']
        password=request.json['password']
        if '@' not in email:
            abort(400,'帳號或密碼格式錯誤或其他原因')
        try:
            mycursor.execute(select_user+" where email like %s",(email,))
        except:
            conn.close()
            abort(500,'伺服器錯誤') #return error
        else:
            get_first=mycursor.fetchone()
            if get_first==None:
                print('not exist')
                mycursor.execute("INSERT INTO user (name,email,password) VALUES (%s,%s,%s)",(name,email,password))
                conn.commit()
                
                #session紀錄
                mycursor.execute(select_user+" where email like %s and password like %s",(email,password))
                get_first=mycursor.fetchone()
                for key,value in zip(session_keys,get_first[:3]):
                    session[key]=value
                json_data['ok']=True
            else:
                conn.close()
                abort(400,'信箱已有人使用或其他原因') #return error
        
    elif request.method=='PATCH':
        print('patch user')
        conn=db.get_connection()
        mycursor=conn.cursor()
        email=request.json['email']
        password=request.json['password']
        if '@' not in email:
            abort(400,'帳號或密碼錯誤或其他原因')
        try:
            mycursor.execute(select_user+' where email like %s and password like %s',(email,password))
        except:
            abort(500,'伺服器錯誤') #return error
        else:
            get_first=mycursor.fetchone()
            conn.close()
            if get_first==None:
                abort(400,'帳號或密碼錯誤或其他原因') #return error
            else:
                for key,value in zip(session_keys,get_first[:3]):
                    session[key]=value
                print('session',session)
                json_data['ok']=True

    elif request.method=='DELETE':
        print('delete user')
        print(session)
        for key in session_keys:
            session.pop(key)
        if 'data' in session:
            session.pop('data')
        print('delete',session)
        json_data['ok']=True
    else:
        abort(400,'request method error') #return error
    return jsonify(json_data),200
