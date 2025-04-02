from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    # 邮箱验证相关字段
    email_verified = models.BooleanField(_('邮箱已验证'), default=False)
    verification_token = models.CharField(_('验证令牌'), max_length=64, blank=True)
    token_sent_time = models.DateTimeField(_('令牌发送时间'), null=True)

