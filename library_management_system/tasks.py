from celery import shared_task
from django.core.management import CommandError, call_command
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_reminders(self):
    try:
        # 记录任务开始时间
        start = timezone.now()
        logger.info(f"开始执行到期提醒任务 {start}")
        # 调用管理命令（推荐方式）
        call_command('send_overdue_reminders')
        # 计算耗时
        duration = timezone.now() - start
        logger.info(f"任务完成，耗时 {duration.total_seconds()} 秒")
        return True
    except CommandError as exc:
        # 处理命令不存在的逻辑，例如记录日志或发送通知
        print(f"CommandError: {exc}")
        # 根据需要决定是否重试或标记为失败
        if self.request.retries < self.max_retries:
            self.retry(exc=exc, countdown=60 * 5)  # 5分钟后重试，但限制重试次数
        else:
            # 达到最大重试次数，标记任务为失败
            self.update_state(state='FAILURE', meta={'exc': str(exc)})

    except Exception as exc:
        logger.error(f"任务失败: {str(exc)}")
        self.retry(exc=exc, countdown=60 * 5)  # 5分钟后重试
