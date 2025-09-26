import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
def get_connection():
     return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
def create_table():
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS USERS (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USERNAME VARCHAR(20) UNIQUE NOT NULL,
                EMAIL VARCHAR(30) UNIQUE NOT NULL,
                PASSWORD VARCHAR(255) NOT NULL );
                """
            )
        conn.commit()
    finally:
        conn.close()
def find_user_id(username):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="SELECT ID FROM USERS WHERE USERNAME=%s"
            cursor.execute(sql,(username,))
            return cursor.fetchone()
    finally:
        conn.close()
def insert_user(username,password,email):
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
             hashed_password=generate_password_hash(password)
             sql="INSERT INTO USERS (USERNAME,PASSWORD,EMAIL) VALUES(%s,%s,%s)"
             cursor.execute(sql,(username,hashed_password,email))
        conn.commit()
    finally:
        conn.close()
def find_user(username):
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
            sql=" SELECT * FROM USERS WHERE USERNAME=%s"
            cursor.execute(sql,(username,))
            return cursor.fetchone()
    finally:
        conn.close()
def find_user_email(email):
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
            sql="SELECT * FROM USERS WHERE EMAIL=%s"
            cursor.execute(sql,(email,))
            return cursor.fetchone()
    finally:
        conn.close()
def check_password(stored_password,given_password):
    return check_password_hash(stored_password,given_password)
def update_password(password,email):
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
             hashed_password=generate_password_hash(password)
             sql="UPDATE USERS SET PASSWORD=%s WHERE EMAIL=%s "
             cursor.execute(sql,(hashed_password,email,))
        conn.commit()   
    finally:
        conn.close()
def create_notes_table():
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
             cursor.execute(
                 """
                CREATE TABLE  IF NOT EXISTs NOTES (
                ID INT AUTO_INCREMENT PRIMARY KEY ,
                USERNAME VARCHAR(30) NOT NULL,
                NOTES_TITLE VARCHAR(200)NOT NULL,
                CONTENT  TEXT NOT NULL,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES USERS(USERNAME) ON DELETE CASCADE
                );
                """  
             )
        conn.commit()
    finally:
        conn.close()
def insert_notes(username,title,content):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="INSERT INTO NOTES (USERNAME,NOTES_TITLE,CONTENT) VALUES (%s,%s,%s)"
            cursor.execute(sql,(username,title,content,))
        conn.commit()
    finally:
        conn.close()
def find_notes(username):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="SELECT * FROM NOTES WHERE USERNAME=%s"
            cursor.execute(sql,(username,))
            return cursor.fetchall()
    finally:
        conn.close()
def find_notes_id(id):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="SELECT * FROM NOTES WHERE ID=%s"
            cursor.execute(sql,(id,))
            return cursor.fetchone()
    finally:
        conn.close()
def deleteNote(id):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="DELETE  FROM NOTES WHERE ID=%s"
            cursor.execute(sql,(id,))
        conn.commit()
    finally:
        conn.close()
        
def updateNote(title,content,id):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="UPDATE NOTES SET NOTES_TITLE=%s ,CONTENT=%s WHERE ID=%s"
            cursor.execute(sql,(title,content,id))
        conn.commit()
    finally:
        conn.close()
def create_files_table():
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS FILES(
                FILE_ID INT AUTO_INCREMENT PRIMARY KEY,
                USERNAME VARCHAR(30) NOT NULL,
                FILE_NAME VARCHAR(255) NOT NULL,
                FILE_PATH  VARCHAR(500) NOT NULL,
                UPLOADED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (USERNAME) REFERENCES USERS(USERNAME) ON DELETE CASCADE
                )
                """
            )
        conn.commit()
    finally:
        conn.close()
def insert_files_table(username,filename,filepath):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="INSERT INTO FILES (USERNAME,FILE_NAME,FILE_PATH) VALUES (%s,%s,%s)"
            cursor.execute(sql,(username,filename,filepath,))
        conn.commit()
    finally:
        conn.close()

def find_file(username):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="SELECT * FROM files WHERE USERNAME=%s"
            cursor.execute(sql,(username,))
            return cursor.fetchall()
    finally:
        conn.close()
def find_file_id(fid):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="SELECT * FROM files WHERE FILE_ID=%s"
            cursor.execute(sql,(fid,))
            return cursor.fetchone()
    finally:
        conn.close()
def delete_file_id(fid):
    try:
        conn=get_connection()
        with conn.cursor() as cursor:
            sql="DELETE  FROM FILES WHERE FILE_ID=%s"
            cursor.execute(sql,(fid,))
        conn.commit()
    finally:
        conn.close()
def db_search(query, username):    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM 
        NOTES WHERE 
        ( NOTES_TITLE LIKE %s OR CONTENT LIKE %s) 
        AND 
        USERNAME = %s
        ''',(f'%{query}%', f'%{query}%',username)
    )    
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return notes

    
        










