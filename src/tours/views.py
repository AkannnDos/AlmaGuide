from django.db.models import F

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from tours.models import Tour
from tours.serializers import TourSerializer


class TourViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TourSerializer
    permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.action == 'my_tours':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'my_tours':
            return Tour.objects.filter(
                orders__user=self.request.user
            ).annotate(
                title=F(f'title_{self.request.LANGUAGE_CODE}'),
                description=F(f'description_{self.request.LANGUAGE_CODE}'),
                way_to_travel=F(f'way_to_travel_{self.request.LANGUAGE_CODE}')
            )
        return Tour.objects.all().annotate(
            title=F(f'title_{self.request.LANGUAGE_CODE}'),
            description=F(f'description_{self.request.LANGUAGE_CODE}'),
            way_to_travel=F(f'way_to_travel_{self.request.LANGUAGE_CODE}')
        )

    @action(methods=['get'], detail=False, url_name='my-tours',
            url_path='my')
    def my_tours(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

