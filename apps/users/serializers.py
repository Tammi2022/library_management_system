from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User


class UserSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=128, required=True, write_only=True)
    email = serializers.CharField(max_length=128, required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    phone = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'password', 'email', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
