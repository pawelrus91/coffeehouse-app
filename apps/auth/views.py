from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from apps.auth.serializers import LoginSerializer, MeSerializer, RegisterSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            'message': _('User was successfully registered.'),
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # TODO: remove `is_active` after implemented activation system
        serializer.save(is_active=True)


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class MeAPIView(generics.ListAPIView):
    serializer_class = MeSerializer

    def get_queryset(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
