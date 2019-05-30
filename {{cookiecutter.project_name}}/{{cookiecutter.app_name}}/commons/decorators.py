import os
import requests
from functools import wraps
from flask import request
from {{cookiecutter.app_name}}.commons.exceptions import AuthError
from {{cookiecutter.app_name}}.config import ACCEPTED_CLAIMS_SET

JWT_VALIDATION_ENDPOINT = os.getenv("JWT_VALIDATION_ENDPOINT")


def _get_token_auth_header(auth):
    """Obtains the Access Token from the Authorization Header
    """
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            token = _get_token_auth_header(request.headers.get('authorization'))
            response = requests.get(JWT_VALIDATION_ENDPOINT, headers={'authorization': "Bearer " + token})
            response.raise_for_status()
            if not validate_claims(response.json()['claims']):
                raise AuthError({"code": "invalid_claims",
                                "description": "The access token did not provided "
                                               "the required claims to access resource."}, 401)
        except Exception as e:
                raise AuthError({"description": "token rejected",
                                 "errors": str(e)}, 401)
        return f(*args, **kwargs)
    return wrap


def validate_claims(response_claims):
    """Determines if the required scope is present in the Access Token
    Args:
        response_claims(str): The scope required to access the resource
    """
    response_claims_set = set(response_claims)
    if len(response_claims_set.intersection(ACCEPTED_CLAIMS_SET)) > 0:
        return True
    return False
