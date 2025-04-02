import os
from celery import Celery
from django.conf import settings

# 设置 Django 配置环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')

app = Celery('library_management_system')

# 使用 Django 的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有 Django app 中的任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
