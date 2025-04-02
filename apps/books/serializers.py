from rest_framework import serializers

from apps.books.models import Book


class BookSerializers(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200, required=True)
    isbn = serializers.CharField(max_length=13, required=True)
    category = serializers.CharField(max_length=50, required=True)
    author = serializers.CharField(max_length=100, required=True)
    publisher = serializers.CharField(max_length=100, required=True)
    publish_date = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Book
        fields = '__all__'
