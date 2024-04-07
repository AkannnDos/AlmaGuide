from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from reviews.filters import AttractionReviewFilterSet, TourReviewFilterSet
from reviews.models import AttractionReview, TourReview
from reviews.serializers import (
    AttractionReviewCreateSerializer, ReviewRetrieveSerializer,
    TourReviewCreateSerializer
)


class AttractionReviewViewSet(CreateModelMixin, ListModelMixin,
                              GenericViewSet):
    serializer_class = ReviewRetrieveSerializer
    permission_classes = (AllowAny,)
    filterset_class = AttractionReviewFilterSet
    queryset = AttractionReview.objects.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return AttractionReviewCreateSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()
    

class TourReviewViewSet(CreateModelMixin, ListModelMixin,
                              GenericViewSet):
    serializer_class = ReviewRetrieveSerializer
    permission_classes = (AllowAny,)
    filterset_class = TourReviewFilterSet
    queryset = TourReview.objects.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TourReviewCreateSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()
