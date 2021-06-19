import mysql.connector 
from config import bucket_name,AWSAccessKeyId,AWSSecretKey,cdn_domain,rds_host,rds_user,rds_password
from werkzeug.utils import secure_filename
from flask import *
import os
import boto3
from data.createDBTable import createDB

posts=Blueprint('post',__name__)
@posts.route('/post', methods=['GET','POST'])
def post():
    
    if request.method=='POST':
        print(123)
        text=request.form['text']
        img=request.files['file']
        if img:
            print(img)
            filename = secure_filename(img.filename)
            print(filename)
            print(img.content_type)
            cdn_url=cdn_domain+filename
            print(cdn_url)
            # print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_link=save_to_s3(AWSAccessKeyId,AWSSecretKey,img,cdn_domain)
        cursor,db=check_db_and_table(rds_host,rds_user,rds_password)
        save_to_rds(cursor,db,text,img_link)
        return redirect('/post')
    if request.method=='GET':
        cursor,db=check_db_and_table(rds_host,rds_user,rds_password)
        posts=select_from_rds(cursor)
        
        return render_template('post.html',posts=posts)
                  
def save_to_s3(AWSAccessKeyId,AWSSecretKey,img,cdn_domain):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretKey
    )
    
    s3.upload_fileobj(
        img,
        bucket_name,
        img.filename,
        ExtraArgs={
            "ACL": "public-read", #Access control list
            "ContentType": img.content_type
        }
    )
    img_link=f'https://{cdn_domain}/{img.filename}'
    return img_link

def check_db_and_table(host,user,password):
    db=mysql.connector.connect(
        host=host,
        user=user, 
        password=password
    )
    cursor=db.cursor()

    # create db if db is not exist
    db_name='taipei_day_trip_post'
    createDB(cursor,db_name)
    # change db
    db.database=db_name
    
    # create table posts if posts is not exist
    table_name='posts'
    cursor.execute('show tables')
    tables=cursor.fetchall() # [(table,),(table,)]
    print(tables)
    ct=0
    
    for table in tables:
        if len(tables)==0:
            break
        if table_name in table[0]:
            print(f'table "{table_name}" exist')
            break
        else:
            ct+=1
    #if no table or posts not in table
    if ct==len(tables):
        cursor.execute("""CREATE TABLE posts (
            id bigint PRIMARY KEY AUTO_INCREMENT,
            text TEXT CHARACTER SET utf8mb4 NOT NULL,
            img_link VARCHAR(255)
        )""")
        print(f'table "{table_name}" created')
    return cursor,db
    
def save_to_rds(cursor,db,text,url):
    #save 
    cursor.execute('insert into posts (text,img_link) values (%s,%s)',(text,url))
    db.commit()
    db.close()

def select_from_rds(cursor):
    cursor.execute('select * from posts')
    get_data=cursor.fetchall()
    print(get_data)
    posts=[]
    for data in get_data:
        dict_data={}    
        dict_data['id']=data[0]
        dict_data['text']=data[1]
        dict_data['img_link']=data[2]
        posts.append(dict_data)
    posts.reverse()
    return posts
    