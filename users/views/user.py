from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers.user import UserMeSerializer


class UserViewSet(viewsets.ViewSet):

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = UserMeSerializer(user)
        return Response(serializer.data)
