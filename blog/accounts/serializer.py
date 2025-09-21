from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from accounts.models import User, Roles


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'first_name', 'last_name',
                  'country_code', 'password', 'role']
        
        extra_kwargs = {
            'password': {'write_only': True},  # Don't expose password in response
        }

    def create(self, validated_data):
        # Hash the password before saving the user
        # validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user