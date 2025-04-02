from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from apps.book_record.models import BookRecord
from apps.books.models import Book
from apps.users.models import User
class BookRecordShowSerializers(serializers.ModelSerializer):

    class Meta:
        model = BookRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].read_only = True

class BookBorrowSerializers(serializers.ModelSerializer):
    # 显式定义外键字段（客户端提交 user_id/book_id 而非对象）
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',  # 映射到模型的 user 字段
        write_only=True
    )
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',  # 映射到模型的 book 字段
        write_only=True
    )
    due_date = serializers.DateField(
        required=False,
        default=lambda: timezone.now().date() + timedelta(days=30),
        help_text="应还日期（默认30天后）"
    )

    class Meta:
        model = BookRecord
        fields = ['user_id','book_id','due_date']
        extra_kwargs = {
            # borrow_date 由模型 auto_now_add=True 自动处理，客户端无需提交
            'borrow_date': {'read_only': True}
        }

    def validate(self, attrs):
        """可选：添加自定义验证逻辑"""
        # 示例：检查书籍是否已归还（return_date 为空表示未归还）
        book = attrs['book']
        if BookRecord.objects.filter(book=book, return_date__isnull=True).exists():
            raise serializers.ValidationError("该书已被借出，暂不可借")
        return attrs

