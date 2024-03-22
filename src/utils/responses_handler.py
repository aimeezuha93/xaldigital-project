import simplejson
from flask import Response


def return_error_response(
    status_code=404, message="An internal error occurred", **kwargs
):
    output = {"status": "error", "message": message, **kwargs}
    dump_response = simplejson.dumps(output, default=str)
    return Response(
        response=dump_response, status=status_code, mimetype="application/json"
    )


def return_successful_response(data, status_code=200, **kwargs):
    output = {"status": "success", "data": data, **kwargs}
    dump_response = simplejson.dumps(output, default=str)
    return Response(
        response=dump_response, status=status_code, mimetype="application/json"
    )
