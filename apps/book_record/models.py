from django.contrib.auth.models import User
from django.db import models

from apps.books.models import Book
from apps.users.models import User
from apps.utils.time_mixin import TimeMixin


class BookRecord(TimeMixin):  # 图书借阅记录
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField('借出时间', auto_now_add=True)
    due_date = models.DateField('应还日期')
    return_date = models.DateField('归还时间', null=True, blank=True)
    renew_count = models.PositiveIntegerField('续借次数', default=0)

    def __str__(self):
        return f"{self.user.username} - {self.book}"

    class Meta:
        verbose_name = 'book_record'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['borrow_date', 'due_date']),
        ]
        db_table = "book_record"
