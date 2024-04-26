from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'full_name', 'phone_number', 'email', 'password',
            'photo'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance
    

class SignUpResponseSerializer(serializers.Serializer):
    user_data = UserCreateSerializer()
    refresh = serializers.CharField()
    access = serializers.CharField()


class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    photo = serializers.ImageField()


class ForgotEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class ChangePasswordlSerializer(serializers.Serializer):
    password = serializers.CharField()
