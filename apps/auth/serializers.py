from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {
                    'password': _('The password and confirmation password must match.'),
                },
            )
        return data

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True}}
