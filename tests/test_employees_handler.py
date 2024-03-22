import os
import sys
import json
import inspect
import pytest
from unittest.mock import patch

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


@pytest.mark.usefixtures("test_app")
class TestEndpoints(object):
    @patch("src.employees_handler.EmployeeOperations.__init__", lambda self: None)
    @patch("src.employees_handler.EmployeeOperations.get", lambda self, email: None)
    def test_get_employee(self):
        response = self.app.get("/employees/lperin@perin.org")
        assert response.status_code == 200

    @patch("src.employees_handler.EmployeeOperations.__init__", lambda self: None)
    @patch("src.employees_handler.EmployeeOperations.post", lambda self: None)
    def test_add_employee(self):
        body_request = {
            "data": {
                "first_name": "Pepito",
                "last_name": "Piedras",
                "company_name": "La Rojeña",
                "address": "Colinas de Santa Monica 1234",
                "city": "Mateos",
                "state": "NL",
                "zip": 9568,
                "phone1": "55-89-02-76",
                "phone2": "56-30-84-63",
                "email": "pedrito_piedras@yahoo.com",
                "department": "Operations",
            }
        }
        response = self.app.post(
            "/employees",
            data=json.dumps(body_request),
            content_type="application/json",
        )
        assert response.status_code == 200

    patch("src.employees_handler.EmployeeOperations.__init__", lambda self: None)

    @patch("src.employees_handler.EmployeeOperations.put", lambda self, email: None)
    def test_update_employee(self):
        body_request = {"data": {"department": "Marketing"}}
        response = self.app.put(
            "/employees/jamal@vanausdal.org",
            data=json.dumps(body_request),
            content_type="application/json",
        )
        assert response.status_code == 200

    patch("src.employees_handler.EmployeeOperations.__init__", lambda self: None)

    @patch("src.employees_handler.EmployeeOperations.delete", lambda self, email: None)
    def test_delete_employee(self):
        response = self.app.delete("/employees/elly_morocco@gmail.com")
        assert response.status_code == 200
