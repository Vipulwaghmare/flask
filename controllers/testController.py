from flask import request, jsonify
from model.UserModel import UserModel
from services.User import User

from utils.requestValidation import validate_request_body


def first_test(): 
  return 'test'

def second_test(): 
  return { 'error': 'user' },400

