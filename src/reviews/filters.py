from django_filters import rest_framework as filters

from reviews.models import AttractionReview, TourReview


class AttractionReviewFilterSet(filters.FilterSet):

    class Meta:
        model = AttractionReview
        fields = ('attraction', )

    
class TourReviewFilterSet(filters.FilterSet):

    class Meta:
        model = TourReview
        fields = ('tour', )
