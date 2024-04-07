from django.contrib.auth.models import update_last_login

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserCreateSerializer, SignUpResponseSerializer


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