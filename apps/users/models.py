from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.utils.time_mixin import TimeMixin


class User(AbstractUser):
    registration_date = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = 'users'
        verbose_name_plural = verbose_name


class Book(TimeMixin):  # 图书基本信息
    title = models.CharField('书名', max_length=200, db_index=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, db_index=True)
    category = models.CharField('分类', max_length=50)
    author = models.CharField('作者', max_length=100)
    publisher = models.CharField('出版社', max_length=100)
    publish_date = models.DateField('出版日期')
    cover = models.ImageField('封面', null=True, blank=True)
    description = models.TextField('简介', blank=True)
    STATUS_CHOICES = (
        (1, '正常'),
        (2, '借出'),
        (3, '销毁'),
    )
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    class Meta:
        verbose_name = 'books'
        verbose_name_plural = verbose_name
        db_table = "books"
