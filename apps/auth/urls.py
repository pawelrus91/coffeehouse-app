from django.urls import path
from rest_framework import routers

from apps.auth import views

app_name = 'auth'
router = routers.SimpleRouter()


urlpatterns = [
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/register/', views.RegisterAPIView.as_view(), name='register'),
    path('auth/me/', views.MeAPIView.as_view(), name='me'),
    *router.urls,
]
