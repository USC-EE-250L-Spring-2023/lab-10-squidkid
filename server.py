from flask import Flask, request, jsonify
from main import process1, process2


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

@app.route('/process1', methods=['POST'])
def route_process1():
    data = request.get_json()  # Get data from request
    result = process1(data)  # Call process1 function with the data
    return jsonify(result)  # Return the result as JSON response

@app.route('/process2', methods=['POST'])
def route_process2():
    data = request.get_json()  # Get data from request
    result = process2(data)  # Call process2 function with the data
    return jsonify(result)  # Return the result as JSON response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# TODO: Create a flask app with two routes, one for each function.
# The route should get the data from the request, call the function, and return the result.
