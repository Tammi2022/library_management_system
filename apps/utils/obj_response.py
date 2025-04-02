from django.db import transaction


class ObjectResp:
    @staticmethod
    def value_of(code=None, message=None, **response):
        if code is None:
            code = 200
        if message is None:
            message = "SUCCESS."
        return ObjectResp.response(code, message, **response)

    @staticmethod
    def response(code=None, message=None, **response):
        result = {
            'code': code,
            'message': message,
            'data': response
        }
        if code == 200:
            transaction.commit()
        else:
            transaction.rollback()
        return result
