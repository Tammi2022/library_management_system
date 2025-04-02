# test_celery.py
import pytest
from django.test import override_settings

from apps.book_record.models import BookRecord
from apps.books.models import Book
from apps.users.models import User


@pytest.mark.django_db  # 如果测试涉及数据库操作
@override_settings(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_TASK_ALWAYS_EAGER=True,
)
def test_send_reminders():
    # 关键：在覆盖配置后重新加载 Celery 应用
    from celery import current_app
    current_app.config_from_object('django.conf:settings', namespace='CELERY')
    user = User.objects.create_user(
        username="alicia",
        email="alicia.lx@qq.com",
        password="123",
        phone="13800138000"
    )
    book = Book.objects.create(
        title="The Django Book",
        isbn="The Django Book111111111111",
        category="test",
        author="Jane Developer",
        publisher="Jane Developer publisher",
        publish_date="2023-01-15"
    )
    record = BookRecord.objects.create(
        user=user,
        book=book,
        due_date="2025-04-04"
    )
    # 确认配置已加载
    assert current_app.conf.broker_url == 'redis://localhost:6379/0'

    # 导入任务并执行测试
    from library_management_system.tasks import send_reminders
    result = send_reminders.delay()
    assert result.successful()
