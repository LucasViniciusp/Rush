from __future__ import nested_scopes
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from rest_framework.viewsets import GenericViewSet

from rush import serializers
from rush import models


# Create your views here.
class RegisterViewSet(viewsets.generics.CreateAPIView, GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterUserSerializer
