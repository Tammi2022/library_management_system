import logging
from enum import Enum

from apps.utils.api_error import ApiError
from apps.utils.obj_response import ObjectResp

logger = logging.getLogger('error')


def get_error_response_dict(e):
    if type(e) == BadRequestError:
        response_dict = ObjectResp.response(code=400, message=e.error_type, details=e.details)
    elif type(e) == TypeError:
        response_dict = ObjectResp.response(code=400, message='类型错误', details=str(e))
    else:
        response_dict = ObjectResp.response(code=400, message='error', details=str(e))
    return response_dict


class BadRequestError(ApiError):

    def __init__(self, error_type, details=None):
        self.error_type = error_type
        self.status_code = 400
        self.response_message = "Bad Request"
        if details:
            self.details = details
        logger.error(f"error_type:{self.error_type}\ndetails:{self.details}")


class ERRTITLEENUM(Enum):
    ERREXP = "__simpleError__ :"
    SERVEXP = "__servError__ :"


# 错误异常
class ErrorException(Exception):
    def __init__(self, msg):
        self.msg = f"""{ERRTITLEENUM.ERREXP.value}{msg}"""

    def __str__(self):
        return self.msg


# 服务异常
class ServException(Exception):
    def __init__(self, msg):
        self.msg = f"""{ERRTITLEENUM.SERVEXP.value}{msg}"""

    def __str__(self):
        return self.msg
