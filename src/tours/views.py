from django.db.models import F

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from tours.models import Tour
from tours.serializers import TourSerializer


class TourViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TourSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return Tour.objects.all().annotate(
            title=F(f'title_{self.request.LANGUAGE_CODE}'),
            description=F(f'description_{self.request.LANGUAGE_CODE}'),
            way_to_travel=F(f'way_to_travel_{self.request.LANGUAGE_CODE}')
        )
