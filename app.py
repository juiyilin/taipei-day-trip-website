from flask import *
import jinja2
import mysql.connector 
from mysql.connector.pooling import MySQLConnectionPool

from data.dbconfig import user,password
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


db=MySQLConnectionPool(
	host='localhost',
	user=user, 
	password=password, # change config when upload
	database='taipeispot',
	pool_name='my_connection_pool',
	pool_size=10,
	pool_reset_session=True
)
select_spot='select * from spot'

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route('/api/attractions')
def get_attraction():
	result={}
	page=request.args.get('page','')
	keyword=request.args.get('keyword','')
	try:
		page=int(page)					
		# 筆數			
		conn,mycursor=db_connect()
		mycursor.execute(f'select count(*) from spot where name like "%{keyword}%"')
		num=mycursor.fetchone()[0]
		
		select=select_spot
		if keyword!='':
			select+=f' where name like "%{keyword}%"'
		select+=f' order by id limit {page*12}, 12'
		mycursor.execute(select)
	
	except:
		abort(500)
	else:
		data=list(mycursor)
		column_names=mycursor.column_names #tuple
		db_close(conn,mycursor)
		spots=[]
		# print(data)
		num_data=len(data)
		for i in range(num_data):
			dt=list(data[i])
			spot=spot_handle(dt,column_names)
			spots.append(spot)
			
		result['data']=spots #data:[{spot1},{spot2}]
		if num-(page*12+num_data)>0:
			next_page=page+1
		else:
			next_page=None
		result['nextPage']=next_page
		return jsonify(result),200
	
@app.route('/api/attraction/',defaults={'attractionid':''})
@app.route('/api/attraction/<attractionid>')
def get_attraction_by_id(attractionid):
	if attractionid=='' or attractionid=='0':
		return redirect('/api/attraction/1')
	try:
		attractionid=int(attractionid)
	except:
		abort(400)
	else:
		result={}
		select=f'{select_spot} where id ={attractionid}'
	try:
		conn,mycursor=db_connect()
		mycursor.execute(select)
		data=list(list(mycursor)[0])
	
	except:
		abort(500)
	else:
		column_names=mycursor.column_names #tuple
		db_close(conn,mycursor)
		spot=spot_handle(data,column_names)
		result['data']=spot #data:{spot}
	return jsonify(result),200


# function
def spot_handle(data,column_names):
	data[-3]=float(data[-3])
	data[-2]=float(data[-2])
	data[-1]=data[-1].split()
	spot={}
	for key,d in zip(column_names,data):
		spot[key]=d
	return spot

def db_connect():
	conn=db.get_connection()
	mycursor=conn.cursor()
	return conn,mycursor

def db_close(conn,mycursor):
	mycursor.close()
	conn.close()

# error handle
@app.errorhandler(400)
def input_error(error):
	result={}
	result['error']=True
	result['message']='錯誤'
	return jsonify(result), 400

@app.errorhandler(500)
def server_error(error):
	result={}
	result['error']=True
	result['message']='伺服器錯誤:'+str(error)
	return jsonify(result),500
    
    

app.run(host="0.0.0.0", port=3000,debug=True)