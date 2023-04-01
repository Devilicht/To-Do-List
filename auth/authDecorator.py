# from flask import Flask, request, jsonify
# #from authentication import decode_token
# def auth_decorator(func):
#     def auth():
#         token = request.headers.get("Authorization")
#         isLogged = decode_token(token, "anytoken")
#         if isLogged == None:
#             return jsonify({"message": "no user logged"}), 401
#         func()
#     return auth

from flask import Flask, request, jsonify
from auth.authentication import decode_token

def auth_decorator(func):
    def auth():
        token = request.headers.get("Authorization")
        isLogged = decode_token(token, "anytoken")
        if isLogged == None:
            return jsonify({"message": "no user logged"}), 401
        return func()
    return auth()
