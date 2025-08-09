from rest_framework import serializers
from django.contrib.auth import get_user_model

# This automatically gets our CustomUser model
User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'skills', 'availability']

    def create(self, validated_data):
        # Creates the user using Django's built-in create_user method
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            skills=validated_data.get('skills', ''),
            availability=validated_data.get('availability', True)
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'skills', 'availability', 'profile_image']
        read_only_fields = ['username', 'email']
