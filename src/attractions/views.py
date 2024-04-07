from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Prefetch, F

from drf_yasg.utils import swagger_auto_schema

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from attractions.filters import AttractionFilterSet
from attractions.models import Attraction, Detail
from attractions.serializers import (
    AttractionListSerializer, AttractionDetailSerializer
)
from utils.manual_parameters import QUERY_LATITUDE, QUERY_LONGITUDE


class AttractionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = AttractionListSerializer
    permission_classes = (AllowAny, )
    filterset_class = AttractionFilterSet


    # defaul values
    latitude = 43.237099
    longitude = 76.906639

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AttractionDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user_location = Point(self.longitude, self.latitude, srid=4326)
        qs = Attraction.objects.all().annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}'),
            description=F(f'description_{self.request.LANGUAGE_CODE}'),
            distance=Distance('location', user_location),
            category_icon=F('subcategory__category__icon')
        )
        if self.action == 'retrieve':
            return qs.prefetch_related(
                Prefetch(
                    'details',
                    queryset=Detail.objects.order_by().annotate(
                        name=F(f'name_{self.request.LANGUAGE_CODE}'),
                        value=F(f'value_{self.request.LANGUAGE_CODE}'),
                    )
                )
            )
        return qs
    
    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE]
    )
    def list(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        self.latitude = float(query_params.get('lat'))
        self.longitude = float(query_params.get('lng'))
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE]
    )
    def retrieve(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        self.latitude = float(query_params.get('lat'))
        self.longitude = float(query_params.get('lng'))
        return super().retrieve(request, *args, **kwargs)

