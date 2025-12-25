from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response


class TokenViewSet(viewsets.ViewSet):
    """
    ViewSet for obtaining auth token
    """
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
