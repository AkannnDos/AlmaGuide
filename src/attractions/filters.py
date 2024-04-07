from django_filters import rest_framework as filters

from attractions.models import Attraction


class AttractionFilterSet(filters.FilterSet):

    class Meta:
        model = Attraction
        fields = ('subcategory', )
