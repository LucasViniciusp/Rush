from rest_framework import serializers
from rush import models


# Create serializers here.
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ('username', 'gender', 'birth_date', 'picture', 'banner',)

    def get_username(self, obj):
        return obj.user.username


class RegisterUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = models.User
        fields = ('id','profile', 'email', 'username', 'first_name', 'last_name', 'date_joined',)
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True}, 
            'last_name': {'required': True}
        }

    def validate_profile(self, profile_data):
        profile = ProfileSerializer(data=profile_data)

        if profile.is_valid():
            return profile_data
        raise serializers.ValidationError(profile.errors)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        email = validated_data.get('email')

        user = models.User.objects.create(**validated_data)
        models.Profile.objects.create(user=user, email=email, **profile_data)

        return user
