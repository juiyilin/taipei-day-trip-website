from flask import *
import jinja2
from attraction_api import attraction
from user_api import user_account
from booking_api import booking
from orders_api import order
import os 

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
app.register_blueprint(attraction,url_prefix='/api')
app.register_blueprint(user_account,url_prefix='/api')
app.register_blueprint(booking,url_prefix='/api')
app.register_blueprint(order,url_prefix='/api')
app.secret_key = os.urandom(24)


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

# error handle
@app.errorhandler(400)
def input_error(error):
	result={}
	result['error']=True
	result['message']=error.description
	return jsonify(result), 400

@app.errorhandler(403)
def input_error(error):
	result={}
	result['error']=True
	result['message']=error.description
	return jsonify(result), 400

@app.errorhandler(500)
def server_error(error):
	result={}
	result['error']=True
	result['message']=error.description
	return jsonify(result),500
    
    
app.run(host="0.0.0.0", port=3000)#,debug=True)