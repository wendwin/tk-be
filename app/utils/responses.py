from flask import jsonify

def success_response(message="OK", data=None, meta=None,code=200):
    response = {
        "success": True,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    if meta is not None:
        response["meta"] = meta

    return jsonify(response), code


def error_response(message="Error", errors=None, code=400):
    response = {
        "success": False,
        "message": message
    }

    if errors:
        response["errors"] = errors

    return jsonify(response), code