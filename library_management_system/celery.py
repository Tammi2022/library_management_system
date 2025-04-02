# celery.py (主模块)
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')

app = Celery('library_management_system')

# 打印配置加载状态
print("正在加载 Celery 配置...")
app.config_from_object('django.conf:settings', namespace='CELERY')
print("Broker URL:", app.conf.broker_url)  # 应为 'redis://localhost:6379/0'

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
