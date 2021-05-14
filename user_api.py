from flask import *
import os
from mysql.connector.pooling import MySQLConnectionPool
from data.dbconfig import user,password

user_account=Blueprint('user',__name__)
user_account.secret_key = os.urandom(24)
session={
    'id':None,
    'name':None,
    'email':None,
}
db=MySQLConnectionPool(
	host='localhost',
	user=user, 
	password=password, # change config when upload
	database='users',
	pool_name='my_connection_pool',
	pool_size=10,
	pool_reset_session=True
)
select_user='select * from user'
@user_account.route('/user', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def check_user():
    json_data={}
    
    if request.method=='GET':
        print('get')
        json_data['data']=session
        
    elif request.method=='POST':
        print('post')
        conn=db.get_connection()
        mycursor=conn.cursor()
        name=request.json['name']
        email=request.json['email']
        password=request.json['password']
        try:
            mycursor.execute(f'{select_user} where email like "{email}"')
        except:
            conn.close()
            abort(500,'伺服器錯誤') #return error
        else:
            get_first=mycursor.fetchone()
            if get_first==None:
                print('not exist')
                mycursor.execute(f'INSERT INTO user (name,email,password) VALUES ("{name}","{email}","{password}")')
                conn.commit()
                conn.close()
                json_data['ok']=True
            else:
                conn.close()
                abort(400,'信箱已有人使用') #return error
        
    elif request.method=='PATCH':
        print('patch')
        conn=db.get_connection()
        mycursor=conn.cursor()
        email=request.json['email']
        password=request.json['password']
        try:
            mycursor.execute(f'{select_user} where email like "{email}" and password like "{password}"')
        except:
            abort(500,'伺服器錯誤') #return error
        else:
            get_first=mycursor.fetchone()
            conn.close()
            if get_first==None:
                abort(400,'帳號或密碼錯誤') #return error
            else:
                for key,value in zip(session.keys(),get_first[:3]):
                    session[key]=value
                print('session',session)
                json_data['ok']=True

    elif request.method=='DELETE':
        print('delete')
        for key in session.keys():
            session[key]=None
        json_data['ok']=True
    else:
        abort(400,'request method error') #return error
    return jsonify(json_data),200
