from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.serializers import OrderCreateSerializer, OrderSetPaidSerializer


class OrderViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'set_paid':
            return OrderSetPaidSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['post'], detail=False, url_name='set-paid',
            url_path='set-paid')
    def set_paid(self, request, *args, **kwargs):
        serializer = OrderSetPaidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data.get('order')
        if instance.user == request.user:
            instance.paid = True 
            instance.save(update_fields=['paid'])
            return Response({'message': 'OK'})
        raise PermissionDenied
