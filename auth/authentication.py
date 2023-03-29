
from datetime import datetime,timedelta
import jwt



def generate_token(user_id, key):
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=60)}
    token = jwt.encode(payload, key)
    return token

def decode_token(token, key):
    try:
        decoded_token = jwt.decode(token, key, algorithms=['HS256'])
        return decoded_token
    except jwt.exceptions.DecodeError:
        return None