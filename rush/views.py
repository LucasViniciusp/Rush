from rest_framework import viewsets, status, mixins
from rest_framework.viewsets import GenericViewSet

from rush import serializers
from rush import models


# Create your views here.
class RegisterViewSet(viewsets.generics.CreateAPIView, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterUserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
