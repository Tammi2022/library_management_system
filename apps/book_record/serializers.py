from rest_framework import serializers

from apps.book_record.models import BookRecord


class BookRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookRecord
        fields = '__all__'
