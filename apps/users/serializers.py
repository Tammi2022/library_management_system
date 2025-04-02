from rest_framework import serializers

from apps.users.models import User


class UserSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'password']

