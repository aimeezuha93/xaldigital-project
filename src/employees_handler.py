from flask_restful import Resource
from flask import request
from src.employees.db_handler import DbOperations
from src.utils.responses_handler import (
    return_error_response,
    return_successful_response,
)


class EmployeeOperations(Resource):
    def post(self):
        r = request.get_json(force=True)
        data = r.get("data")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        company_name = data.get("company_name")
        address = data.get("address")
        city = data.get("city")
        state = data.get("state")
        zip = data.get("zip")
        phone1 = data.get("phone1")
        phone2 = data.get("phone2")
        email = data.get("email")
        department = data.get("department")
        try:
            DbOperations().save_in_db(
                first_name,
                last_name,
                company_name,
                address,
                city,
                state,
                zip,
                phone1,
                phone2,
                email,
                department,
            )
            return return_successful_response(
                data={"message": "Employee inserted successfully"}, status_code=200
            )
        except Exception as e:  # noqa
            return return_error_response(400, [e])

    def get(self, email):
        try:
            result = DbOperations().get_from_db(email)
            return return_successful_response(status_code=201, data=result)
        except Exception as e:  # noqa
            return return_error_response(400, [e])

    def put(self, email):
        r = request.get_json(force=True)
        data = r.get("data")
        department = data.get("department")
        try:
            DbOperations().update_from_db(email, department)
            return return_successful_response(
                data={"message": "Employee updated successfully"}, status_code=200
            )
        except Exception as e:  # noqa
            return return_error_response(400, [e])

    def delete(self, email):
        try:
            DbOperations().delete_from_db(email)
            return return_successful_response(
                data={"message": "Employee deleted successfully"}, status_code=200
            )
        except Exception as e:  # noqa
            return return_error_response(400, [e])
