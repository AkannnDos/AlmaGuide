from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from exchanges.models import Exchange
from exchanges.serializers import ExchangeSerializer


class ExchangeRateView(ListModelMixin, GenericViewSet):
    queryset = Exchange.objects.all()
    pagination_class = None
    serializer_class = ExchangeSerializer
