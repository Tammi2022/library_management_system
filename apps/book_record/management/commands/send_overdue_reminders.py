from django.core.management.base import BaseCommand

from apps.utils.notifications import send_overdue_reminders


class Command(BaseCommand):
    help = 'Django 管理命令：发送图书到期提醒'

    def handle(self, *args, **options):
        self.stdout.write("开始查询到期记录...")

        try:
            count = send_overdue_reminders()
            self.stdout.write(
                self.style.SUCCESS(f"成功发送 {count} 条提醒")
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"发送失败: {str(e)}")
            )
            raise
