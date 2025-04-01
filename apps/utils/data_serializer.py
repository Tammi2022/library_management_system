import json
import logging
import re
from datetime import datetime
from decimal import Decimal
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import serializers

from apps.utils.error_util import BadRequestError

logger = logging.getLogger('utils')

class SerializerUtils:
    def __init__(self, instance, page=1, page_size=10):
        self.instance = instance
        self.page_size = page_size
        self.page = page

    def paging_fun(self):
        paginator = Paginator(self.instance, self.page_size)
        # 尝试获取指定页的对象，如果不存在则返回第一页（或根据需要进行处理）
        try:
            page_obj = paginator.page(self.page)
        except PageNotAnInteger:
            # 如果请求的页码不是整数，返回第一页
            page_obj = paginator.page(1)
        except EmptyPage:
            # 如果请求的页码超出页数，返回最后一页
            page_obj = paginator.page(paginator.num_pages)
        return page_obj