from flask import Blueprint
from controllers.testController import first_test, second_test
from model.Logger import Logger

from utils.requestValidation import validate_request_body

logger = Logger.get_instance() 

testRoutes = Blueprint('testRoutes', __name__)

testRoutes.route("/first", methods=["POST"]) (first_test)
testRoutes.route("/second", methods=["POST"]) (second_test)