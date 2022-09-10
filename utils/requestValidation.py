from jsonschema import  validate
from flask import jsonify, request, json
import os

def validate_request_body(route):
    def wrapper(*args, **kwargs):
        if "Content-Type" not in request.headers:
            return jsonify({ "error": "Content-Type header is not set"}),400
        if request.headers['Content-Type'] != "application/json":
            return jsonify({ "error" : "Unsupported media type "}), 415
        try:
            request.get_json()
            return route(*args, **kwargs)
        except Exception as e:
            print("E",e)
            return jsonify({ "error": "Error getting json out of request" }),400
    return wrapper

def validate_request_properties(properties):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                request_data = request.get_json()
                missing_values = []
                for data in properties:
                    if data not in request_data:
                        missing_values.append(data)
                if (len(missing_values) == 1):
                    return jsonify({ "error": f"Missing value in request : {missing_values[0]}" }), 400
                elif (len(missing_values) > 1):
                    return jsonify({ "error": f"Missing values in request : {tuple(missing_values)}" }), 400
            except Exception as e:
                return jsonify({ "error" : "Error in validating request" }), 500 
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator

def validate_request_schema(schema_file_path):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                request_data = request.get_json()
                basedir = os.getcwd()
                file_name = os.path.join(basedir, schema_file_path )
                json_schema = json.load(open(file_name))
                validate(instance=request_data, schema=json_schema)
            except Exception as e:
                error = e.schema["error_msg"] if "error_msg" in e.schema else e.message
                return jsonify({ "error" : f"Error in request {error}" }), 500 
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator