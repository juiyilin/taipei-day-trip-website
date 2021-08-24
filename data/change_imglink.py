import mysql.connector 


db=mysql.connector.connect(
    host='localhost',
    user=user, #change
    password=password, #change
    database='taipeispot'
)
cursor=db.cursor()
cursor.execute('select images from spot')
links=cursor.fetchall()
print(len(links))
for i in range(len(links)):
    newlink=links[i][0].replace('http','https')
    # print(newlink)
    cursor.execute('update spot set images=%s where id=%s',(newlink,i+1))
db.commit()

db.close()