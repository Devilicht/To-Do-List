from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os 
from datetime import datetime

app = Flask(__name__)

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    dbname='tasks_db',
    user='postgres',
    password='3030'
)
cur = conn.cursor()

@app.route('/users', methods = ['POST'])
def users():
    email= request.form['email']
    password = request.form['password']

    cur.execute('SELECT password FROM users WHERE email=%s', (email,))
    result = cur.fetchone()
    conn.commit()
    cur.close()

    if result is not None and check_password_hash(result[0], password):
        return 'Login bem sucedido!'
    else:
        return 'Usuário ou senha incorretos'
    
    

@app.route('/users/register', methods =['POST']) 
def register():
    name = request.form ['name']
    email = request.form ['email']
    password = request.form ['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return 'as senhas não coincidem'
    
    hashed_password = generate_password_hash(password)

    cur.execute('INSERT INTO users (name,email, password) VALUES (%s,%s,%s)',(name,email, hashed_password))
    conn.commit()
    cur.close()   



#@app.route('users/myTasks', methods = ['GET'])
#def tasks():


app.run()   
