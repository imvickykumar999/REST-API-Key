# apiapp/views.py
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .models import APIKey, Item
from .serializers import UserSerializer, APIKeySerializer, ItemSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)  # Ensure Token creation
            api_key = APIKey.objects.get(user=user).key
            return Response({'token': token.key, 'api_key': str(api_key)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT', 'DELETE']:
            return [APIKeyPermission()]
        return [permissions.AllowAny()]


class APIKeyPermission(permissions.BasePermission):
    """
    Custom permission to only allow CRUD operations if API key is provided in headers.
    """

    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        if api_key:
            return APIKey.objects.filter(key=api_key).exists()
        return False

