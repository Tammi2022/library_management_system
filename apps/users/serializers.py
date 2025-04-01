from rest_framework import serializers

from apps.books.models import Book


class BookModelSerializers(serializers.ModelSerializer):

    class Meta:
        model = Book  # 代表使用哪个模型类做校验
        fields = '__all__'

