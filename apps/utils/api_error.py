from django.db import transaction
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """ Base ApiError class that allows simple formatting
    of error responses without boilerplate. """

    def __init__(self):
        self.error_type = f'{self.__module__}.{self.__class__.__name__}'

        if not hasattr(self, 'details'):
            self.details = {}

        if not hasattr(self, 'status_code'):
            raise NotImplementedError(f'{self.error_type} must have a `status_code` (HTTP Status Code)')

        if not hasattr(self, 'response_message'):
            raise NotImplementedError(f'{self.error_type} must have a `response_message` (Response Message)')

        super().__init__(self.response_message)


def handle_api_error(fn):
    def wrapper(*args, **kwargs):
        try:
            with transaction.atomic():
                result = fn(*args, **kwargs)
                return result
        except TimeoutError as e:
            logger.error(f"Timeout: {e}")
            return JsonResponse({'type': 'Timeout Error', "code": 503, "message": "请求超时"}, status=503)
        except ApiError as e:
            # 捕获 ApiError 异常并记录日志
            logger.error(f"ApiError: {e.error_type}, Details: {e.details}", exc_info=True)
            # 返回错误响应
            return JsonResponse({
                'type': e.error_type,
                'code': e.status_code,
                'message': e.response_message,
                'details': e.details,
            }, status=e.status_code)
        except Exception as e:
            # 捕获其他未处理的异常
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            # 返回通用错误响应
            error = {
                'type': 'Internal Server Error',
                'code': 500,
                'message': 'An error has occurred and we are looking into it.',
                'details': str(e),  # 添加异常详细信息
            }
            return JsonResponse(error, status=500)

    return wrapper
