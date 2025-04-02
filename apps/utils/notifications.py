import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from apps.book_record.models import BookRecord
from library_management_system.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

logger = logging.getLogger('apps')


def send_overdue_reminders():
    """符合 Django 最佳实践的邮件发送"""
    from django.db import connection
    logger.info(f"Database: {connection.settings_dict['NAME']}")
    today = timezone.localdate()
    logger.info(f"today is {today}")
    seven_day = today + timezone.timedelta(days=6)
    logger.info(f"seven_day is {seven_day}")
    today_str = today.isoformat()  # 格式如 "2025-04-02"
    seven_day_str = seven_day.isoformat()
    records = BookRecord.objects.filter(
        status=1,
        due_date__range=(today_str, seven_day_str)
    ).select_related('user', 'book')
    logger.info(f"""records len is {len(records)}""")
    sent_count = 0
    from django.conf import settings
    print(f"SMTP 服务器: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    import smtplib
    try:
        with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            print("连接成功！")
    except Exception as e:
        print(f"错误: {str(e)}")
    import smtplib
    try:
        with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
            server.login("tammii@163.com", "")  # 替换为实际值
            server.sendmail(
                from_addr="tammii@163.com",
                to_addrs=["tammiii@163.com"],  # 改为真实邮箱
                msg="Subject: This is a test email"
            )
        print("邮件发送成功")
    except Exception as e:
        print(f"错误详情: {str(e)}")

    for record in records:
        logger.info(f"sending reminder for {record.user}")
        context = {
            'username': record.user.get_short_name(),
            'book_title': record.book.title,
            'due_date': record.due_date.strftime("%Y-%m-%d")
        }
        # 渲染 HTML 模板
        html_content = render_to_string(
            'emails/overdue_reminder.html',
            context
        )
        # 创建邮件对象
        email_add = record.user.email
        email_add = "tammiii@163.com"
        logger.info(f"email_add is {email_add}")
        email = EmailMultiAlternatives(
            subject="图书到期提醒",
            body="纯文本备用内容",  # 自动生成纯文本版本
            # body=html_content,  # 自动生成纯文本版本
            from_email="tammii@163.com",
            to=[email_add]
        )
        email.attach_alternative(html_content, "text/html")
        import smtplib, socket
        try:
            email.send(fail_silently=False)
        except smtplib.SMTPResponseException as e:
            error_code = e.smtp_code
            error_message = e.smtp_error.decode()
            logger.error(f"SMTP 协议错误 {error_code}: {error_message}")
        except smtplib.SMTPServerDisconnected:
            logger.error("服务器意外断开连接")
        except Exception as e:
            logger.exception("未知错误")  # 记录完整堆栈跟踪
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP 认证失败：密码错误或未启用客户端授权")
        except socket.timeout:
            logger.error("连接超时：检查防火墙或网络策略")
        try:
            record.last_reminder = timezone.now()
            record.save(update_fields=['last_reminder'])
            sent_count += 1
        except Exception as e:
            # 记录到 Django 日志系统
            logger.error(f"邮件发送失败至 {record.user.email}: {str(e)}")
    return sent_count
