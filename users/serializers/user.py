from rest_framework import serializers

from users.models import User


class UserMeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
        ]
