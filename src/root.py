from flask_restful import Resource
from flask import Response
import simplejson


class WelcomeMessage(Resource):
    def get(self):
        return {
            "status": "OK",
            "message": "This project belongs to user Aimee Zuniga",
            "version": "1.0.0",
        }


class Status(Resource):
    def get(self):
        output = {"status": "OK"}
        dump_response = simplejson.dumps(output, default=str)
        return Response(response=dump_response, status=200, mimetype="application/json")
