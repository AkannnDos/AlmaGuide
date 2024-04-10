from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Prefetch, F

from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from attractions.models import Attraction
from categories.models import Category, Subcategory
from categories.serializers import (
    CategoryListSerializer, SubcategoryListSerializer
)
from utils.manual_parameters import QUERY_LATITUDE, QUERY_LONGITUDE


class CategoryViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CategoryListSerializer
    permission_classes = (AllowAny, )
    
    def get_queryset(self):
        return Category.objects.filter(is_popular=False).annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}')
        )

    @action(methods=['get'], detail=False, url_name='popular',
            url_path='popular')
    def get_popular_list(self, request, *args, **kwargs):
        qs = Category.objects.filter(is_popular=True).annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}')
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class SubcategoryListView(ListModelMixin, GenericViewSet):
    serializer_class = SubcategoryListSerializer
    permission_classes = (AllowAny, )

    # defaul values
    latitude = 43.237099
    longitude = 76.906639

    def get_queryset(self):
        user_location = Point(self.longitude, self.latitude, srid=4326)
        return Subcategory.objects.order_by('order').annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}')
        ).prefetch_related(
            Prefetch(
                'attractions',
                queryset=Attraction.objects.filter(is_on_main=True).annotate(
                    category_icon=F('subcategory__category__icon'),
                    distance=Distance('location', user_location)
                )
            )
        )
    
    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE]
    )
    def list(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        self.latitude = float(query_params.get('lat'))
        self.longitude = float(query_params.get('lng'))
        return super().list(request, *args, **kwargs)
