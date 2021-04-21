import mysql.connector 
from dbconfig import user,password
import json

db = mysql.connector.connect(
    host="localhost",
    user=user,
    password=password
)
mycursor = db.cursor()
try:
    mycursor.execute("create database taipeispot")
    
except mysql.connector.errors.DatabaseError:
    print('already exist')
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
except:
    print('table exist')

with open('taipei-attractions.json',encoding='utf8') as jsonfile:
    data=json.loads(jsonfile.read())
#spot=data['result']['results'][91]
for spot in data['result']['results']:
    # print(spot['RowNumber'],spot['stitle'],spot['CAT2'],spot['xbody'],spot['address'],spot['info'],spot['MRT'],spot['latitude'],spot['longitude'],sep='\n')
    img_str=spot['file'].replace('.JPG','.jpg').split('http')[1:]
    images=''
    for img_url in img_str:
        if (img_url.endswith('jpg') or img_url.endswith('png')):
            # print('http'+img_url)
            images+='http'+img_url+' '
    # print(images)
    insert="INSERT INTO spot (id, name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
    value=(spot['RowNumber'],spot['stitle'],spot['CAT2'],spot['xbody'],spot['address'],spot['info'],spot['MRT'],spot['latitude'],spot['longitude'],images)
    mycursor.execute(insert,value)
    db.commit()
    print(mycursor.rowcount, "record inserted.")
print('finish')
db.close()
