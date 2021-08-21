from flask import *
import time
from datetime import datetime
import urllib.request
import json
from database import db_connect,db_close,db
from config import partner_key



order=Blueprint('orders',__name__)


def compare_date(post_date):
    input_date_list=list(map(int,post_date.split('-')))
    today=datetime.now().date()
    input_date=datetime(input_date_list[0], input_date_list[1], input_date_list[2]).date()
    return input_date<today #if True,abort 400

@order.route('/orders', methods=['POST'])
def orders():
    if 'id' not in session:
        # print(session)
        abort(403,'未登入系統')
    else:
        json_data={}
        if request.method=='POST':
            print('post orders')
            number=time.strftime('%Y%m%d%H%M%S', time.localtime()) #訂單號碼
            # print(request.json) prime,order

            # check date and time
            trip_time=request.json['order']['trip']['time']
            print(trip_time!= 'morning' and trip_time!='afternoon')
            print(compare_date(request.json['order']['trip']['date']))
            if (trip_time != 'morning' and trip_time != 'afternoon') or compare_date(request.json['order']['trip']['date']):
                abort(400,'訂單建立失敗')
            
            # check email
            if '@' not in request.json['order']['contact']['email']:
                abort(400,'訂單建立失敗')

            # create order
            try:
                conn,mycursor=db_connect(db)
                session_id=session['id']
                trip_order=str(request.json['order']).replace("'",'"')
                mycursor.execute("INSERT INTO orders (number, user_id, trip_order, status) VALUES(%s,%s,%s,1)",(number,session_id,trip_order))
            except:
                db_close(conn,mycursor)
                abort(400,'訂單建立失敗')
            else:
                conn.commit()

            # TapPay API
            url='https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
            values = {
                "prime": request.json['prime'],
                "partner_key": partner_key,
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
                'x-api-key': partner_key
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
                mycursor.execute('UPDATE orders SET status = 0 WHERE number = %s',(number,))
                conn.commit()
                session.pop('data')
                print('付款成功')

            else:
                print('付款失敗')

            db_close(conn,mycursor)
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
            conn,mycursor=db_connect(db)
            mycursor.execute('SELECT * FROM orders WHERE user_id=%s',(session["id"],))
            get_all=mycursor.fetchall()
            db_close(conn,mycursor)

            # print(get_all[0])
            print(get_all)
            if get_all==[]:
                json_data['data']=[]
            else:
                order_list=[]
                for order in get_all:
                    data={}
                    print('error',order)
                    trip=json.loads(order[2])
                    data['number']=order[0]
                    data['price']=trip['price']
                    data['trip']=trip['trip']['attraction']['name']
                    data['date']=trip['trip']['date']
                    data['status']=order[3]
                    order_list.append(data)
                order_list.reverse()
                json_data['data']=order_list
            # print(json_data)
        else:
            conn,mycursor=db_connect(db)
            mycursor.execute('SELECT number, trip_order, status FROM orders WHERE user_id=%s AND number=%s',(session["id"],orderNumber))
            get_one=mycursor.fetchone()
            db_close(conn,mycursor)

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