import mysql.connector
from datetime import datetime
import random

my_password = ''

def create_database():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS mathlife_database")
    db.commit() 
    mycursor.close()
    db.close()

def create_table():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor = db.cursor()
    mycursor.execute(f"CREATE TABLE IF NOT EXISTS user_data(id INT PRIMARY KEY AUTO_INCREMENT, username text, password text, coins int, hintPotion int , toolPotion int, lifePotion int)")
    mycursor.execute(f"CREATE TABLE IF NOT EXISTS mail_data(id INT PRIMARY KEY AUTO_INCREMENT, sender text, title text, content text, time datetime)")
    mycursor.execute(f"CREATE TABLE IF NOT EXISTS geometry_problem(id INT PRIMARY KEY AUTO_INCREMENT, problem text, hint text, tool text, answer int)")
    mycursor.execute(f"CREATE TABLE IF NOT EXISTS shop_data(id INT PRIMARY KEY AUTO_INCREMENT, item text, price int)")
    
    # akun kepsek
    if not username_exists('kepsek'):
        insert_user('kepsek' , 'kepsek#1234')
        
    # item shop default
    if not item_exists('hintPotion'):
        insert_shop('hintPotion' , 10)
    if not item_exists('toolPotion'):
        insert_shop('toolPotion' , 20)
    if not item_exists('lifePotion'):
        insert_shop('lifePotion' , 30)    
        
    # problem geo default
    if not problem_exists('geometry_problem','Tentukan besar sudut eksterior total dari sebuah segitiga sembarang!'):
        insert_problem('geometry_problem',
                       'Tentukan besar sudut eksterior total dari sebuah segitiga sembarang!',
                       'Besar sudut eksterior total dari sembarang poigon konveks adalah 360°',
                       'https://www.geogebra.org/calculator/uz7mjstg?embed',
                       360)
    if not problem_exists('geometry_problem','Diberikan segitiga ABC sehingga AB=AC. Jika sudut ABC adalah 50°, tentukan besar sudut BAC!'):
        insert_problem('geometry_problem',
                       'Diberikan segitiga ABC sehingga AB=AC. Jika sudut ABC adalah 50°, tentukan besar sudut BAC!',
                       'Besar sudut interior total dari segitiga sembarang adalah 180°, lalu gunakan sudut ABC = sudut ACB',
                       'https://www.geogebra.org/calculator/aag87jaf?embed',
                       80)
    if not problem_exists('geometry_problem','Diberikan persegi ABCD. Titik E di dalamnya sehingga CDE sama sisi, tentukan besar sudut AEB!'):
        insert_problem('geometry_problem',
                       'Diberikan persegi ABCD. Titik E di dalamnya sehingga CDE sama sisi, tentukan besar sudut AEB!',
                       'Sudut interior segitiga sama sisi adalah 60°, sedangkan persegi adalah 90°, lalu gunakan ADE dan BCE sama kaki',
                       'https://www.geogebra.org/calculator/gvm4pat2?embed',
                       150)
    if not problem_exists('geometry_problem','Diberikan lingkaran dengan pusat O. Titik ABC pada lingkaran sehingga sudut BAC adalah 60°, tentukan besar sudut ABO + sudut ACO!'):
        insert_problem('geometry_problem',
                       'Diberikan lingkaran dengan pusat O. Titik ABC pada lingkaran sehingga sudut BAC adalah 60°, tentukan besar sudut ABO + sudut ACO!',
                       'Sudut pusat lingkaran adalah 2 kali sudut kelilingnya sehingga sudut BOC adalah 120°, lalu gunakan besar sudut interior total dari segitiga sembarang adalah 180°',
                       'https://www.geogebra.org/calculator/juvs2wng?embed',
                       60)
    if not problem_exists('geometry_problem','Diberikan segi empat ABCD. Titik E dan F berturut-turut pada BC dan AB sehingga AF=BF=CF dan BE=CD. Tentukan besar sudut EDF!'):
        insert_problem('geometry_problem',
                       'Diberikan segi empat ABCD. Titik E dan F berturut-turut pada BC dan AB sehingga AF=BF=CF dan BE=CD. Tentukan besar sudut EDF!',
                       'Gunakan fakta segitiga CDE kongruen segitiga BEF, lalu gunakan DE=EF sehingga DEF sama kaki',
                       'https://www.geogebra.org/calculator/ez5v2ts3?embed',
                       45)

    db.commit() 
    mycursor.close()
    db.close()
    
def length(table_name: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM {table_name}")
    result = mycursor.fetchall() 
    return len(result)

def insert_user(username: str , password: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor = db.cursor()
    mycursor.execute(f"INSERT INTO user_data (username, password, coins, hintPotion, toolPotion, lifePotion) VALUES(%s,%s,%s,%s,%s,%s)", (username,password,0,0,0,0,))
    db.commit() 
    mycursor.close() 
    db.close()

def update_user(coins: int, hintPotion: int, toolPotion: int, lifePotion: int, username: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"UPDATE user_data SET coins=%s, hintPotion=%s, toolPotion=%s, lifePotion=%s WHERE username=%s", (coins,hintPotion,toolPotion,lifePotion,username,))
    db.commit()
    mycursor.close() 
    db.close()

def get_user(username: str) -> list :
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM user_data WHERE username=%s", (username,))
    result = mycursor.fetchall()
    
    return [result[0][i] for i in range(7)]

def get_user_all() -> list[list] :
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM user_data")
    result = mycursor.fetchall()
    
    return [[result[i][j] for j in range(7)] for i in range(len(result))]

def username_exists(username: str) -> bool:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM user_data WHERE username=%s", (username,))
    result = mycursor.fetchall() 
    if len(result) > 0:
        return True 
    else:
        return False 
    
def insert_problem(table_name: str, problem: str, hint: str, tool: str, answer: int):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor = db.cursor()
    mycursor.execute(f"INSERT INTO {table_name} (problem, hint, tool, answer) VALUES(%s,%s,%s,%s)",(problem,hint,tool,answer,))
    db.commit() 
    mycursor.close() 
    db.close()
    
def problem_exists(table_name: str,problem: str) -> bool:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM {table_name} WHERE problem=%s", (problem,))
    result = mycursor.fetchall() 
    if len(result) > 0:
        return True 
    else:
        return False 

def get_problem(table_name: str, id: int) -> list:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM {table_name} WHERE id=%s",(id,))
    result = mycursor.fetchall()
    return [result[0][i] for i in range(5)]

def insert_mail(sender: str, title: str, content: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor = db.cursor()
    mycursor.execute(f"INSERT INTO mail_data (sender, title, content, time) VALUES(%s,%s,%s,%s)",(sender,title,content,datetime.now(),))
    db.commit() 
    mycursor.close() 
    db.close()    

def get_mail(sender: str) -> list[list]:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM mail_data WHERE sender=%s or sender=%s", (sender,'kepsek',))
    result = mycursor.fetchall() 
    return [[result[len(result)-1-i][j] for j in range(5)] for i in range(len(result))]

def get_mail_all() -> list[list]:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM mail_data")
    result = mycursor.fetchall() 
    return [[result[len(result)-1-i][j] for j in range(5)] for i in range(len(result))]

def random_number(amount: int,min: int, max: int) -> list:
    list_number = []
    while len(list_number) < amount:
        number = random.randint(min,max)
        if not (number in list_number):
            list_number += [number]
    return list_number

def item_exists(item: str) -> bool:
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM shop_data WHERE item=%s", (item,))
    result = mycursor.fetchall() 
    if len(result) > 0:
        return True 
    else:
        return False 
    
def get_shop_price():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM shop_data")
    result = mycursor.fetchall() 
    return [result[i][2] for i in range(len(result))]   

def insert_shop(item: str,price: int):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor = db.cursor()
    mycursor.execute(f"INSERT INTO shop_data (item, price) VALUES(%s,%s)", (item,price,))
    db.commit() 
    mycursor.close() 
    db.close()
    
def update_shop(hintPotionPrice: int, toolPotionPrice: int, lifePotionPrice: int):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = my_password,
        database = 'mathlife_database'
    )
    mycursor = db.cursor()
    mycursor.execute(f"UPDATE shop_data SET price=%s WHERE item=%s", (hintPotionPrice,'hintPotion',))
    mycursor.execute(f"UPDATE shop_data SET price=%s WHERE item=%s", (toolPotionPrice,'toolPotion',))
    mycursor.execute(f"UPDATE shop_data SET price=%s WHERE item=%s", (lifePotionPrice,'lifePotion',))
    db.commit() 
    mycursor.close() 
    db.close()
    
create_database()
create_table()