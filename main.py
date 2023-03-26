from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from datetime import datetime,timedelta
import jwt
 

app = Flask(__name__)

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    dbname='tasks_db',
    user='postgres',
    password='3030'
)
cur = conn.cursor()

app.config['SECRET_KEY'] = 'mySecretKey'

def generate_token(user_id):
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token

def decode_token(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded_token
    except jwt.exceptions.DecodeError:
        return None

@app.route('/users', methods=['POST'])
def auth():
    email = request.json['email']
    password = request.json['password']

    cur.execute('SELECT user_id, password FROM users WHERE email=%s', (email,))
    result = cur.fetchone()
    conn.commit()

    if result is not None and check_password_hash(result[1], password):
        token = generate_token(result[0])
        return jsonify({'message': 'Successful login!', 'token': token}), 200
    else:
        return jsonify({'message': 'Incorrect user or password'}), 401

@app.route('/getLoggedUserId', methods=['GET'])
def getLoggedUserId(token):
    token = request.headers.get('Authorization')
    decoded_token = decode_token(token)

    if decoded_token is not None:
        user_id = decoded_token['user_id']
        return  jsonify({'user_id':user_id}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 401
    

@app.route('/register', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.json['confirm_password']

    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match'})

    hashed_password = generate_password_hash(password)

    cur.execute('INSERT INTO users (name,email, password) VALUES (%s,%s,%s)', (name, email, hashed_password))
    conn.commit()

    return jsonify({'message': 'Account added'})

@app.route('/users/<user_id>/tasks', methods=['GET'])
def readTasks(user_id): 
    token=request.headers.get('Authorization')
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']) 
        token = decoded_token['user_id'] 
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid token'}), 401
           
    cur.execute('SELECT tasks.task_id, tasks.title, tasks.description, tasks.is_done FROM tasks INNER JOIN users ON tasks.user_id = users.user_id WHERE users.user_id = %s',user_id)
    tasks = cur.fetchall()
    return jsonify(tasks)

@app.route('/users/<user_id>/tasks/<task_id>', methods=['POST'])
def createTask(user_id):
    user_id = request.headers.get('Authorization') 
    try:
        decoded_token = jwt.decode(user_id, app.config['SECRET_KEY'], algorithms=['HS256']) 
        user_id = decoded_token['user_id'] 
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid token'}), 401
    
    title = request.json['title']
    description = request.json.get('description','')
    
    cur.execute('INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s)', (title, description, user_id))
    conn.commit()

    return jsonify({'message': 'Task created successfully'})

@app.route('/users/<user_id>/tasks/<task_id>', methods=['PUT'])
def updateTitleAndDescription(user_id, task_id):
    token=request.headers.get('Authorization')
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']) 
        token = decoded_token['user_id'] 
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid token'}), 401    
    
    cur.execute('SELECT * FROM tasks WHERE task_id=%s AND user_id=%s', (task_id, user_id))
    task = cur.fetchone()
    if task is None:
        return jsonify({'error': 'Task not found or does not belong to logged user'})
    title = request.json.get('title',)
    description = request.json.get('description',)
    if title == None and description == None:
        cur.execute('UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (task[1], task[2], task_id))
        conn.commit()
    elif title == None and description != None:
        cur.execute('UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (task[1], description, task_id))
        conn.commit()
    elif title != None and description == None:
        cur.execute('UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (title, task[2], task_id))
        conn.commit()
    else:
        cur.execute('UPDATE tasks SET title=%s, description=%s WHERE task_id=%s', (title, description, task_id))
        conn.commit()
    return jsonify({'message': 'Task updated'})

@app.route('/users/<user_id>/tasks/<tasks_id>', methods=['DELETE'])
def delete_task(user_id,task_id):
    user_id = getLoggedUserId()
    
    cur.execute('SELECT * FROM tasks WHERE user_id=%s  task_id=%s', (user_id,task_id))
    task = cur.fetchone()
    if task is None:
        return jsonify({'error': 'Task not found or does not belong to logged user'})

    cur.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
    conn.commit()

    return jsonify({'message': 'Task deleted successfully'})



if __name__=='__main__':
    app.run(debug=True)   
