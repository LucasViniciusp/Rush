from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rush import views


router = routers.DefaultRouter()
router.register(r'register', views.RegisterViewSet, basename='user')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
