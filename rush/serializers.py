from rest_framework import serializers
from rush import models


# Create serializers here.
class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'picture', 'banner',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        print(validated_data)
        return self.Meta.model.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = ('id', 'username', 'name', 'first_name', 'last_name', 'birth_date', 'picture', 'banner',)

    def get_name(self, obj):
        return obj.get_full_name()
    
    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
