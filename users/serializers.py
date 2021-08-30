from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from users import utils

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            User._meta.pk.name)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    re_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    default_error_messages = {
        "password_mismatch": "The two password fields doesn't match"
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            User._meta.pk.name,
            'password',
            're_password')

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("Cannot create user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            if validated_data['password'] == validated_data['re_password']:
                validated_data.pop("re_password")
                user = User.objects.create_user(**validated_data)
                user.is_active = False
                user.save(update_fields=["is_active"])
            else:
                self.fail('password_mismatch')
        return user


class UidTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "uid_invalid": "Invalid user id or user doesn't exist.",
        "token_invalid": "Invalid token for given user."
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = utils.decode_url_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(id=uid)
        except (User.DoesNotExist, ValueError):
            raise ValidationError(
                {"uid": [self.error_messages["uid_invalid"]]}, code="uid_invalid"
            )

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("token", ""))

        if is_token_valid:
            return validated_data
        else:
            raise ValidationError(
                {"token": [self.error_messages["token_invalid"]]}, code="token_invalid"
            )


class ActivationSerializer(UidTokenSerializer):
    default_error_messages = {
        "token_error": "Token for given user is dry."
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_active:
            return attrs
        return PermissionDenied(self.error_messages['token_error'])
