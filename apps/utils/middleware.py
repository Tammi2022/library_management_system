import time
import json
import logging
from datetime import datetime

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('api.monitor')


class APILoggingMiddleware(MiddlewareMixin):
    # 需要排除的请求头
    SAFE_HEADERS = ['CONTENT_TYPE', 'ACCEPT', 'SERVER_PORT']

    # 敏感参数过滤
    SENSITIVE_KEYS = {'password', 'token', 'secret', 'authorization'}

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.exclude_paths = getattr(settings, 'LOG_EXCLUDE_PATHS', [])
        self.slow_threshold = getattr(settings, 'SLOW_REQUEST_THRESHOLD', 3)

    def process_request(self, request):
        if self._should_exclude(request.path):
            return

        # 记录开始时间
        request.start_time = time.time()

        # 初始化日志元数据
        request.meta = {
            'method': request.method,
            'path': request.path,
            'ip': self._get_client_ip(request),
            'user': request.user.username if request.user.is_authenticated else 'anonymous'
        }

    def process_response(self, request, response):
        if self._should_exclude(request.path):
            return response

        # 计算耗时
        duration = time.time() - getattr(request, 'start_time', time.time())

        # 记录慢请求
        if duration > self.slow_threshold:
            logger.warning(f"Slow Request ({duration:.2f}s): {request.meta}")

        # 构建日志数据
        # log_data = {
        #     **request.meta,
        #     'status': response.status_code,
        #     'duration': f"{duration:.3f}s",
        #     'params': self._safe_params(request),
        #     'response': self._safe_response(response)
        # }
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': 'INFO',
            'method': request.method,
            'path': request.path,
            'ip': self._get_client_ip(request),
            'user': request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'guest',
            'status': response.status_code,
            'duration_ms': round(duration * 1000, 2),  # 毫秒数值
            'params': self._safe_params(request),
            'response_size': len(response.content)  # 响应体大小
        }

        # logger.info(json.dumps(log_data, ensure_ascii=False))
        logger.info("API Request", extra=log_data)
        return response

    def _should_exclude(self, path):
        return any(path.startswith(p) for p in self.exclude_paths)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',') if x_forwarded_for else request.META.get('REMOTE_ADDR')

    def _safe_params(self, request):
        """安全获取请求参数"""
        params = {}

        # GET参数处理
        try:
            params['get'] = {
                k: v
                for k, v in request.GET.lists()
                if k not in self.SENSITIVE_KEYS
            }
        except Exception as e:
            params['get'] = f"Error: {str(e)}"

        # POST参数处理
        try:
            if request.content_type == 'application/json':
                params['post'] = self._filter_sensitive(
                    json.loads(request.body.decode('utf-8'))
                )
            elif request.content_type == 'multipart/form-data':
                params['post'] = {
                    k: 'FILE' if isinstance(v, list) else v
                    for k, v in request.POST.lists()
                }
            else:
                params['post'] = self._filter_sensitive(request.POST.dict())
        except Exception as e:
            params['post'] = f"Error: {str(e)}"

        return params

    def _safe_response(self, response):
        """安全获取响应内容"""
        if 400 <= response.status_code < 500:
            try:
                return json.loads(response.content.decode())
            except:
                return response.content.decode()[:200]
        return None

    def _filter_sensitive(self, data):
        """递归过滤敏感字段"""
        if isinstance(data, dict):
            return {k: '&zwnj;***FILTERED***&zwnj;' if k in self.SENSITIVE_KEYS else self._filter_sensitive(v)
                    for k, v in data.items()}
        elif isinstance(data, list):
            return [self._filter_sensitive(item) for item in data]
        return data