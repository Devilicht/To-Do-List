from flask import Flask,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime,timedelta
import jwt

from dotenv import load_dotenv 
from database.repository import UserRepository


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mySecretKey'

userRepository = UserRepository()

def generate_token(user_id):
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=60)}
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

    result = userRepository.findUserByEmail(email=email)
    if result is not None and check_password_hash(result[1], password):
        token= generate_token(result[0])
        return jsonify({'message': 'Successful login!', 'token': token}), 200
    else:
        return jsonify({'message': 'Incorrect user or password'}), 401

@app.route('/getLoggedUserId', methods=['GET'])
def getLoggedUserId():
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
        return jsonify({'message': 'Passwords do not match'}),200
    else:
        401
    hashed_password = generate_password_hash(password)

    userRepository.saveUser(name=name,email=email,hashed_password=hashed_password)

    return jsonify({'message': 'Account added'})

@app.route('/users/<user_id>/tasks', methods=['GET'])
def readTasks(user_id): 
    getLoggedUserId()       
    tasks = userRepository.joinUserTask(user_id=user_id)
    if tasks != []:      
        return jsonify(tasks),200
    else:
        return jsonify ({"message":"no registered tasks"}),401

@app.route('/users/<user_id>/tasks', methods=['POST'])
def createTask(user_id):
    getLoggedUserId()
    
    title = request.json['title']
    description = request.json['description']

    try:
        userRepository.generateTask(title=title, description=description, user_id=user_id)
        
        return jsonify({'message': 'Task created successfully'})
    except KeyError:
        return jsonify({'message' : 'error creating task'}),401

@app.route('/users/<user_id>/tasks/<task_id>', methods=['PUT'])
def updateTitleAndDescription(user_id, task_id):
    getLoggedUserId()
    
    title = request.json.get('title',)
    description = request.json.get('description',)

    task = userRepository.selectTaskById(user_id=user_id, task_id=task_id)
    
    if task is None:
        return jsonify({'error': 'Task not found or does not belong to logged user'})
    
    userRepository.updateTask(title=title, description=description, task=task, task_id=task_id)
    
    return jsonify({'message': 'Task updated'})
    

@app.route('/users/<user_id>/tasks/<task_id>', methods=['DELETE'])
def delete_task(user_id,task_id):
    getLoggedUserId() 
    
    task = userRepository.selectTaskById(user_id=user_id, task_id=task_id)
    if task is None:
        return jsonify({'error': 'Task not found or does not belong to logged user'})

    userRepository.deleteTask(task_id=task_id)

    return jsonify({'message': 'Task deleted successfully'})



if __name__=='__main__':
    app.run(debug=True)   
