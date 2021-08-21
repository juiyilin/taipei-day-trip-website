from flask import *
from database import db_connect,db_close,db

attraction=Blueprint('attraction',__name__)

def spot_handle(data,column_names):
	data[-3]=float(data[-3])
	data[-2]=float(data[-2])
	data[-1]=data[-1].split()
	spot={}
	for key,d in zip(column_names,data):
		spot[key]=d
	return spot


select_spot='select * from spot'

@attraction.route('/attractions')
def get_attraction():
	result={}
	page=request.args.get('page','')
	keyword=request.args.get('keyword','')
	try:
		page=int(page)					
		# 筆數			
		conn,mycursor=db_connect(db)
		mycursor.execute(f'select count(*) from spot where name like "%{keyword}%"')
		num=mycursor.fetchone()[0]
		
		select=select_spot
		if keyword!='':
			select+=f' where name like "%{keyword}%"'
		select+=f' order by id limit {page*12}, 12'
		mycursor.execute(select)
	
	except:
		db_close(conn,mycursor)
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
	
@attraction.route('/attraction/',defaults={'attractionid':''})
@attraction.route('/attraction/<attractionid>')
def get_attraction_by_id(attractionid):
	if attractionid=='' or attractionid=='0':
		return redirect('/api/attraction/1')
	try:
		attractionid=int(attractionid)
	except:
		abort(400,'景點編號不正確')
	else:
		result={}
		select=f'{select_spot} where id ={attractionid}'
	try:
		conn,mycursor=db_connect(db)
		mycursor.execute(select)
		data=list(list(mycursor)[0])
	
	except:
		db_close(conn,mycursor)
		abort(500,'伺服器錯誤')
	else:
		column_names=mycursor.column_names #tuple
		db_close(conn,mycursor)

		spot=spot_handle(data,column_names)
		result['data']=spot #data:{spot}
	return jsonify(result),200