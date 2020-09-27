import flask_restful
from flask import request
from firebase_admin import auth
from functools import wraps
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = request.headers
        try:
            decoded_token = auth.verify_id_token(headers['Authorization'])
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            app.logger.info(e)
            flask_restful.abort(401)

    return wrapper


class AppResource(flask_restful.Resource):
    method_decorators = [authenticate]   # applies to all inherited resources