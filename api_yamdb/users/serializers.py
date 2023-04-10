import re
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions

from .models import YamdbUser, RoleChoices

USERNAME_PATTERN = r'^[\w.@+-]+$'
ME_UNACCEPTABLE_USERNAME = 'Me недопустимое имя пользователя'
UNACCEPTABLE_USERNAME = 'Недопустимое имя пользователя'
UNACCEPTABLE_EMAIL = 'Длина email > 254'
UNACCEPTABLE_ROLE = 'Недопустимая роль'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields["confirmation_code"] = PasswordField()

    def validate_username(self, attrs):
        username_exist = YamdbUser.objects.filter(username=attrs).exists()
        print(username_exist)
        if username_exist:
            return attrs
        raise exceptions.NotFound(
            self.error_messages["no_active_account"],
            "no_active_account",
        )

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.ValidationError(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        data = {}
        refresh = self.get_token(self.user)

        data['token'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class YamdbUserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(ME_UNACCEPTABLE_USERNAME)
        if not re.match(USERNAME_PATTERN, value):
            raise serializers.ValidationError(UNACCEPTABLE_USERNAME)
        return value

    class Meta:
        model = YamdbUser
        fields = ('username', 'email',)


class FullYamdbUserSerialiser(YamdbUserSerializer):
    role = serializers.CharField(required=False, default='user')

    def validate_role(self, value):
        if value in RoleChoices:
            return value
        raise serializers.ValidationError(UNACCEPTABLE_ROLE)

    class Meta:
        model = YamdbUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)


class RestrictRoleYamdbUserSerialiser(FullYamdbUserSerialiser):
    role = serializers.CharField(read_only=True,)
