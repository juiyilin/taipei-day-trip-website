from flask import *
import time
import urllib.request
import json
from mysql.connector.pooling import MySQLConnectionPool
from data.dbconfig import user,password

def db_connect():
	conn=db.get_connection()
	mycursor=conn.cursor()
	return conn,mycursor



db=MySQLConnectionPool(
	host='localhost',
	user=user, 
	password=password, # change config when upload
	database='taipeispot',
	pool_name='my_connection_pool',
	pool_size=10,
	pool_reset_session=True
)

order=Blueprint('orders',__name__)

@order.route('/orders', methods=['POST'])
def orders():
    if 'id' not in session:
        # print(session)
        abort(403,'未登入系統')
    else:
        json_data={}
        if request.method=='POST':
            number=time.strftime('%Y%m%d%H%M%S', time.localtime()) #訂單號碼
            # print(request.json) prime,order

            # create order
            try:
                conn,mycursor=db_connect()
                session_id=session['id']
                trip_order=str(request.json['order']).replace("'",'"')
                mycursor.execute(f"INSERT INTO orders (number, user_id, trip_order, status) VALUES('{number}','{session_id}','{trip_order}',1)")
            except:
                abort(400,'訂單建立失敗')
            else:
                conn.commit()

            # TapPay API
            url='https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
            values = {
                "prime": request.json['prime'],
                "partner_key": 'partner_ccJtfI19TJNYWsxjvHpa7jSWNr31ITdUJlRKVEIUIbv5GSFvTkjcxQQ5',
                "merchant_id": "engineerProject_ESUN",
                "details":"台北一日遊："+request.json['order']['trip']['attraction']['name'],
                "amount": request.json['order']['price'],
                "cardholder": {
                    "phone_number": request.json['order']['contact']['phone'],
                    "name": request.json['order']['contact']['name'],
                    "email": request.json['order']['contact']['email'],
                },
                "order_number":number
            }
            headers={
                'content-type': 'application/json',
                'x-api-key': 'partner_ccJtfI19TJNYWsxjvHpa7jSWNr31ITdUJlRKVEIUIbv5GSFvTkjcxQQ5'
            }
            data = json.dumps(values).encode('ascii') # data should be bytes
            req = urllib.request.Request(url,data,headers)
            with urllib.request.urlopen(req) as response:
                pay_result = response.read().decode('utf8')
            pay_result=json.loads(pay_result)
            print(pay_result)
            json_data['data']={
                    "number": number,
                    "payment": {
                        "status": pay_result['status'],
                        "message":pay_result['msg']
                    }
                }
            if pay_result['status']==0:
                mycursor.execute(f'UPDATE orders SET status = 0 WHERE number = "{number}"')
                conn.commit()
                session.pop('data')
                print('付款成功')

            else:
                print('付款失敗')

            conn.close()
            return jsonify(json_data),200
        else:
            abort(500)


@order.route('/order/',defaults={'orderNumber':''})
@order.route('/order/<orderNumber>')
def get_order(orderNumber):
    if 'id' not in session:
        abort(403,'未登入系統')

    else:
        json_data={}
        if orderNumber=='':
            json_data['data']=None
        else:
            conn,mycursor=db_connect()
            mycursor.execute(f'SELECT number, trip_order, status FROM orders WHERE user_id={session["id"]} AND number="{orderNumber}"')
            get_one=mycursor.fetchone()
            conn.close()
            if get_one==None:
                json_data['data']=None
            else:
                order=json.loads(get_one[1])
                data={}
                data['number']=get_one[0]
                data['price']=order['price']
                data['trip']=order['trip']
                data['contact']=order['contact']
                data['status']=get_one[2]
                json_data['data']=data
        return jsonify(json_data),200