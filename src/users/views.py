import random
import redis
import time

from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import (
    ChangePasswordlSerializer, ForgotEmailSerializer, UserCreateSerializer,
    SignUpResponseSerializer, VerifyOtpSerializer
)
from users.tasks import send_otp_to_email


class SignUpView(CreateModelMixin, GenericViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, )

    @swagger_auto_schema(
        responses={
            201: SignUpResponseSerializer()
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        refresh = RefreshToken.for_user(instance)

        data = {
            'user_data': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        update_last_login(None, instance)
        return Response(data, status=status.HTTP_201_CREATED)
    

class ProfileView(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False, url_name='profile', url_path='me')
    @swagger_auto_schema(
        responses={
            200: UserCreateSerializer()
        }
    )
    def me(self, request):
        serializer = UserCreateSerializer(request.user,
                                          context={'request': request})
        return Response(serializer.data)


class ForgotPasswordViewSet(ViewSet):

    def get_permissions(self):
        if self.action == 'new_password':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(methods=['post'], detail=False, url_name='forgot-request',
            url_path='forgot-password')
    @swagger_auto_schema(request_body=ForgotEmailSerializer())
    def forgot_password(self, request, *args, **kwargs):
        serializer = ForgotEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = self._save_otp(email)
        send_otp_to_email.delay(email, otp)
        return Response({'message': 'OTP sent!'})
    
    @action(methods=['post'], detail=False, url_name='verify-otp',
            url_path='verify-otp')
    @swagger_auto_schema(request_body=VerifyOtpSerializer())
    def verify_otp(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            if self.check_otp(user.email, serializer.validated_data['otp']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            return ValidationError({'detail': _('Incorrect OTP')})
        except User.DoesNotExist:
            raise ValidationError({'detail': _('User not found')})
        
    @action(methods=['post'], detail=False, url_name='new-password',
            url_path='new-password')
    @swagger_auto_schema(request_body=ChangePasswordlSerializer())
    def new_password(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_data': UserCreateSerializer(
                user, context={'request': request}).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    @staticmethod
    def _get_redis():
        return redis.Redis(host='redis', port=6379, db=1)
    
    @staticmethod
    def _generate_otp():
        return random.randint(1000, 9999)

    def _save_otp(self, email) -> int:
        current_time = time.time()
        r = self._get_redis()
        otp = self._generate_otp()
        print(otp)
        r.set(f'otp_{email}', otp)
        r.set(f'otp_{email}_timestamp', current_time)
        r.expire(f'otp_{email}', 60)
        r.expire(f'otp_{email}_timestamp', 60)
        return otp
    
    def check_otp(self, email, otp) -> bool:
        r = self._get_redis()
        in_memory_otp = r.get(f'otp_{email}')
        if in_memory_otp:
            return int(in_memory_otp) == otp
        return False

