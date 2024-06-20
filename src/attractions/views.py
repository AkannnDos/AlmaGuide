from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Prefetch, F, Count, Q, Case, When, Value, \
    BooleanField, IntegerField

from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from attractions.filters import AttractionFilterSet
from attractions.models import Attraction, ChoseAttraction, Detail, Route
from attractions.serializers import (
    AttractionListSerializer, AttractionDetailSerializer,
    ChosenAttractionSerializer, MakeRouteSerializer, RouteListSerializer,
    YandexResponseSerializer
)
from utils.manual_parameters import QUERY_LATITUDE, QUERY_LONGITUDE


class AttractionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ Actions with attractions """
    serializer_class = AttractionListSerializer
    permission_classes = (AllowAny, )
    filterset_class = AttractionFilterSet
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('avg_rate', 'name', 'distance')
    search_fields = (
        'name_en',
        'name_ru',
        'name_kk',
        'description_en',
        'description_ru',
        'description_kk',
    )


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
        ).select_related(
            'subcategory__category'
        )
        if self.action == 'retrieve':
            if self.request.user.is_authenticated:
                favourite_count = Count(
                    'users_chosen__id',
                    filter=(
                        Q(users_chosen__user=self.request.user) & 
                        Q(users_chosen__route__isnull=True)
                    )
                )
            else:
                favourite_count = Value(0, output_field=IntegerField())
            return qs.alias(
                favourite_count=favourite_count
            ).annotate(
                is_favourite=Case(
                    When(favourite_count__gt=0,
                         then=Value(True, output_field=BooleanField())),
                    default=Value(False, output_field=BooleanField())
                )
            ).prefetch_related(
                Prefetch(
                    'details',
                    queryset=Detail.objects.order_by().annotate(
                        name=F(f'name_{self.request.LANGUAGE_CODE}'),
                        value=F(f'value_{self.request.LANGUAGE_CODE}'),
                    )
                ),
                Prefetch(
                    'similar_attractions',
                    queryset=Attraction.objects.all().annotate(
                        name=F(f'name_{self.request.LANGUAGE_CODE}'),
                        description=F(f'description_{self.request.LANGUAGE_CODE}'),
                        distance=Distance('location', user_location),
                    ).select_related(
                        'subcategory__category'
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

    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE]
    )
    @action(methods=['get'], detail=False, url_name='main', url_path='main')
    def get_main(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        self.latitude = float(query_params.get('lat'))
        self.longitude = float(query_params.get('lng'))
        instance = get_object_or_404(self.get_queryset(), **{'is_main': True})
        return Response(self.get_serializer(instance).data)


class FavouriteViewSet(ListModelMixin, GenericViewSet):
    """ Actions with favourite """
    serializer_class = AttractionListSerializer
    permission_classes = (IsAuthenticated, )

    # defaul values
    latitude = 43.237099
    longitude = 76.906639

    def get_serializer_class(self):
        if self.action == 'chose_attraction':
            return ChosenAttractionSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        user_location = Point(self.longitude, self.latitude, srid=4326)
        return Attraction.objects.filter(
            users_chosen__user=self.request.user,
            users_chosen__route__isnull=True
        ).annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}'),
            description=F(f'description_{self.request.LANGUAGE_CODE}'),
            distance=Distance('location', user_location),
        ).select_related(
            'subcategory__category'
        ).order_by('distance')

    @action(methods=['post'], detail=False, url_name='choose',
            url_path='choose')
    def chose_attraction(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE]
    )
    def list(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        self.latitude = float(query_params.get('lat'))
        self.longitude = float(query_params.get('lng'))
        return super().list(request, *args, **kwargs)
    
    @action(methods=['delete'], detail=True, url_name='remove-chosen',
            url_path='chosen')
    def remove_from_chosen(self, request, *args, **kwargs):
        pk = kwargs['pk']
        ChoseAttraction.objects.filter(user=request.user,
                                       attraction_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RouteViewSet(ListModelMixin, GenericViewSet):
    serializer_class = RouteListSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'make_route':
            return MakeRouteSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Route.objects.none()
        return Route.objects.filter(
            user=self.request.user
        ).annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}'),
        ).order_by('-created_at')
    
    def _get_map_url(self, latitude, longitude, queryset):
        url = 'https://yandex.kz/maps/162/almaty/'

        current_location = f'{longitude},{latitude}'
        current_local_location = f'{latitude},{longitude}'
        rtext = '~'.join([
            f'{obj.location.coords[1]},{obj.location.coords[0]}'
            for obj in queryset
        ])

        url_query = f'?l=trf%2Ctrfe&ll={current_location}&mode=routes' \
                    f'&rtext={current_local_location}~{rtext}&rtt=auto' \
                    f'&ruri=~~&z=13.98'
        return url + url_query
    
    @action(methods=['post'], detail=False, url_name='make-routes',
            url_path='make')
    def make_route(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitude = serializer.validated_data['lat']
        longitude = serializer.validated_data['lng']
        user_location = Point(latitude, longitude, srid=4326)

        chosen_attractions = ChoseAttraction.objects.annotate(
            distance=Distance('attraction__location', user_location),
        ).filter(
            user=request.user,
            route__isnull=True,
        ).select_related(
            'attraction'
        ).order_by('distance')
        
        last = chosen_attractions.last()
        if last:
            route = Route.objects.create(
                user=request.user,
                name_en=last.attraction.name_en,
                name_ru=last.attraction.name_ru,
                name_kk=last.attraction.name_kk
            )
            queryset = [item.attraction for item in chosen_attractions]
            chosen_attractions.update(route=route)
            return Response({
                'url': self._get_map_url(latitude, longitude, queryset)
            })
        raise PermissionDenied
    
    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE]
    )
    @action(methods=['get'], detail=True, url_name='route-attractions',
            url_path='attractions')
    def get_attractions(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        latitude = float(query_params.get('lat'))
        longitude = float(query_params.get('lng'))
        pk = kwargs['pk']
        user_location = Point(longitude, latitude, srid=4326)
        queryset = Attraction.objects.filter(
            users_chosen__route_id=pk,
            users_chosen__user=self.request.user,
        ).annotate(
            name=F(f'name_{self.request.LANGUAGE_CODE}'),
            description=F(f'description_{self.request.LANGUAGE_CODE}'),
            distance=Distance('location', user_location),
        ).select_related(
            'subcategory__category'
        ).order_by('distance')
        serializer = AttractionListSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[QUERY_LATITUDE, QUERY_LONGITUDE],
        responses={
            200: YandexResponseSerializer()
        }
    )
    @action(methods=['get'], detail=True, url_name='yandex-maps',
            url_path='yandex')
    def get_yandex_url(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        latitude = float(query_params.get('lat'))
        longitude = float(query_params.get('lng'))
        pk = kwargs['pk']
        user_location = Point(longitude, latitude, srid=4326)
        queryset = Attraction.objects.filter(
            users_chosen__route_id=pk,
            users_chosen__user=self.request.user,
        ).annotate(
            distance=Distance('location', user_location),
        ).order_by('distance')
        return Response({
            'url': self._get_map_url(latitude, longitude, queryset)
        })
        

