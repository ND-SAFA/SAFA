import datetime
import json
from typing import Dict, Optional

import jwt
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api.constants.datetime_constants import duration2days
from api.server.settings import DISABLE_AUTH, JWT_ALGO, ROOT_PASSWORD, SECRET_KEY

"""
Configuration
:prefix: The prefix pre-pending each API key.
:HOUR_SEC: Constants 
"""
PREFIX = "gen"
EXPIRATION_SECONDS = 8 * 3600  # 8 hours / work day.
"""
Keys
"""
EMAIL_KEY = "email"
PASSWORD_KEY = "password"
COOKIE_KEY = "GEN_KEY"
DURATION_KEY = "duration"
EXPIRATION_KEY = "exp"
AUTH_KEY = "key"
ERROR_KEY = "error"


@csrf_exempt
@require_http_methods(["POST"])
def generate_key(request) -> JsonResponse:
    """
    Generates authentication key.
    :param request: The request containing credentials to validate.
    :return: JsonResponse.
    """
    try:
        data = json.loads(request.body)
        email = data.get(EMAIL_KEY)
        password = data.get(PASSWORD_KEY)
        duration = data.get(DURATION_KEY)

        if password != ROOT_PASSWORD:
            return JsonResponse({ERROR_KEY: "Invalid Password."}, status=400)

        if duration not in duration2days:
            return JsonResponse({ERROR_KEY: f"Expected one of {list(duration2days.keys())} but got {duration}"}, status=400)

        key = create_key(duration, email)

        response = JsonResponse({AUTH_KEY: key})
        response.set_cookie(COOKIE_KEY, key, max_age=EXPIRATION_SECONDS, httponly=True)
        return response
    except Exception as e:
        return JsonResponse({ERROR_KEY: str(e)}, status=500)


def create_key(duration: str, email: str):
    """
    Creates API key valid for given email and valid for specified duration.
    :param duration: The duration of the API key.
    :param email: The email to assocaite with key.
    :return:
    """
    days = duration2days[duration]
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    payload = {
        EMAIL_KEY: email,
        EXPIRATION_KEY: exp_date
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGO)
    key = f"{PREFIX}_{encoded_jwt}"
    return key


def decode_key(encoded_key: str) -> Dict:
    """
    Decodes API key and validates that it is still valid.
    :param encoded_key: The API key to decode.
    :return: Decoded payload.
    """
    jwt_token = encoded_key.split('_', 1)[1]
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[JWT_ALGO])
        return payload  # Contains the original information (email, exp, etc.)
    except jwt.ExpiredSignatureError:
        raise ValueError("The key has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid key.")


def authorize_request(request: HttpRequest, data) -> Optional[str]:
    """
    Authorize request using data to extract api key.
    :param request: The request to authorize.
    :param data: The data of the request to authorize.
    :return: Error is something went wrong. None otherwise.
    """
    if DISABLE_AUTH:
        return None

    try:
        if COOKIE_KEY not in request.COOKIES and AUTH_KEY not in data:
            raise Exception(f"Expected `{AUTH_KEY}` to be included in request or cookie `{COOKIE_KEY}` to be set.")
        auth_key = request.COOKIES.get(COOKIE_KEY)
        if auth_key is None:
            auth_key = data[AUTH_KEY]
        if auth_key is None:
            raise Exception(f"Expected `{auth_key}` to contain API key but got null.")
        decode_key(auth_key)
    except Exception as e:
        return str(e)
