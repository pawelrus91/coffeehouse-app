from django.urls import path
from rest_framework import routers

from apps.auth import views

app_name = 'auth'
router = routers.SimpleRouter()


urlpatterns = [
    path('auth/register/', views.RegisterAPIView.as_view(), name='register'),
    *router.urls,
]
