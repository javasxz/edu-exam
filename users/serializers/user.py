from rest_framework import serializers

from users.models import User


class UserMeSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            'display_name',
            "email",
            "phone_number",
            "date_joined",
        )
