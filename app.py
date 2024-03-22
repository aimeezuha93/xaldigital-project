import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from src.root import WelcomeMessage, Status
from src.employees_handler import EmployeeOperations

load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

"""
###########################################
            Welcome
###########################################
"""
api.add_resource(WelcomeMessage, "/")
api.add_resource(Status, "/status")

"""
###########################################
            Employees
###########################################
"""

api.add_resource(EmployeeOperations, "/employees", "/employees/<email>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3001)
