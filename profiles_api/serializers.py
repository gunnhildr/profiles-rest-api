from abc import ABC

from rest_framework import serializers
from profiles_api import models
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _


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


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on")
        # set profile based on user authenticated, so let's make it readonly:
        extra_kwargs = {"user_profile": {"read_only": True}}


class AuthTokenSerializer(serializers.Serializer, ABC):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
