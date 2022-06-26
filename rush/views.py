from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from rush.serializers import RegisterSerializer, UserSerializer, PostSerializer, GroupSerializer
from rush.permissions import UserObjectPermission, GroupPermission
from rush.models import User, Post, Group, GroupMember


# Create your views here.
class RegisterViewSet(CreateAPIView, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    queryset = User.objects.filter(is_active=True)
    filterset_fields = ('username', 'group')
    search_fields = ['content']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, UserObjectPermission)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_active=True)
    filterset_fields = ('user', 'group')
    search_fields = ['content']
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, UserObjectPermission)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    filterset_fields = ('name', 'is_public', 'only_admin_post')
    search_fields = ['name', 'about']
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, GroupPermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            GroupMember.objects.create(group=group, user=request.user, is_admin=True)
    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
