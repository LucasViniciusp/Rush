from rest_framework import serializers
from rush.models import User, Post, Group


# Create serializers here.
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
            "picture",
            "banner",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "first_name",
            "last_name",
            "birth_date",
            "picture",
            "banner",
            "date_joined",
        )

    def get_name(self, obj):
        return obj.get_full_name()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "user", "group", "content", "created_at")
        read_only_fields = ["user"]

    def get_authenticated_user(self):
        return self.context["request"].user

    def validate_group(self, group):
        user = self.get_authenticated_user()
        if group.member.filter(user=user):
            return group

        raise serializers.ValidationError("Not a group member!")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "about",
            "picture",
            "banner",
            "only_admin_post",
            "is_public",
            "created_at",
        )
