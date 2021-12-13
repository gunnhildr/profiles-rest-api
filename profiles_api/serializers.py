from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        # configure serializer to point model serializer to specific models
        # class Meta has to be there
        # list of ALL fields have to be here in Meta
        model = models.UserProfile
        fields = ("id", "email", "name", "password")
        # exception for passord: create on user create, don't allow ti retrieve password hash
        extra_kwargs = {
            "password": {
                "write_only": True,  # won't see in 'get' response
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):  # this is override
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        # set profile based on user authenticated, so let's make it readonly:
        extra_kwargs = {'user_profile': {'read_only': True}}
