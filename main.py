from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
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

@app.route('/getLoggedUserId', methods=['GET'])
def getLoggedUserId():
    user_email = request.headers.get('Authorization')
    cur.execute('SELECT id FROM users WHERE email=%s', (user_email,))
    result = cur.fetchone()
    
    if result is not None:
        return jsonify({'user_id': result[0]}), 200
    else:
        return jsonify({'error': 'Unauthenticated user.'}), 401


@app.route('/users', methods = ['POST'])
def users():
    email= request.json['email']
    password = request.json['password']

    cur.execute('SELECT password FROM users WHERE email=%s', (email,))
    result = cur.fetchone()
    conn.commit()
    cur.close()

    if result is not None and check_password_hash(result[0], password):
        return jsonify({'message': 'Successful login!'})
    else:
         return jsonify({'message': 'Incorrect user or password'})
    

@app.route('/users/register', methods =['POST']) 
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.json['confirm_password']

    if password != confirm_password:
        return jsonify({'message': 'passwords dont match'})
    
    hashed_password = generate_password_hash(password)

    cur.execute('INSERT INTO users (name,email, password) VALUES (%s,%s,%s)',(name,email, hashed_password))
    conn.commit()
    cur.close()   
    return jsonify({'message': 'account added'})


@app.route('/users/myTasks', methods=['POST'])
def createTask():
    user_id = getLoggedUserId()
    
    title = request.json['title']
    description = request.json.get('description', '')
    
    cur.execute('INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s)', (title, description, user_id))
    conn.commit()

    return jsonify({'message': 'Task created successfully'})



@app.route('/users/int:user_id/myTasks', methods=['GET'])
def readTasks():       
    user_id = getLoggedUserId()
    cur.execute('SELECT * FROM tasks WHERE user_id=%s', (user_id,))
    tasks = cur.fetchall()
    return jsonify(tasks)


@app.route('/users/myTasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    user_id = getLoggedUserId()
    
    cur.execute('SELECT * FROM tasks WHERE id=%s AND user_id=%s', (task_id, user_id))
    task = cur.fetchone()
    if task is None:
        return jsonify({'error': 'Task not found or does not belong to logged user'})

    title = request.json.get('title', task[1])
    description = request.json.get('description', task[2])
    is_done = request.json.get('is_done', task[3])

    cur.execute('UPDATE tasks SET title=%s, description=%s, is_done=%s WHERE id=%s', (title, description, is_done, task_id))
    conn.commit()

    return jsonify({'message': 'Task updated'})

@app.route('/users/myTasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = getLoggedUserId()
    
    cur.execute('SELECT * FROM tasks WHERE id=%s AND user_id=%s', (task_id, user_id))
    task = cur.fetchone()
    if task is None:
        return jsonify({'error': 'Task not found or does not belong to logged user'})

    cur.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
    conn.commit()

    return jsonify({'message': 'Task deleted successfully'})



if __name__=='__main__':
    app.run(debug=True)   
