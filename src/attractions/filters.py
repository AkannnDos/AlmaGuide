from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from django_filters.fields import RangeField
from django import forms

from attractions.models import Attraction


class CustomRangeFilter(filters.Filter):
    field_class = RangeField

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        if value:
            if value.start is not None and value.stop is not None:
                lookup_min = "%s__%s" % (self.field_name, 'gte')
                lookup_max = "%s__%s" % (self.field_name, 'lt')
                qs = self.get_method(qs)(**{
                    lookup_min: value.start,
                    lookup_max: value.stop,
                })
                return qs
            elif value.start is not None:
                self.lookup_expr = "gte"
                value = value.start
            elif value.stop is not None:
                self.lookup_expr = "lt"
                value = value.stop
        return super().filter(qs, value)


class AttractionFilterSet(filters.FilterSet):

    avg_rate = CustomRangeFilter()
    category = filters.CharFilter(field_name='subcategory__category_id')

    class Meta:
        model = Attraction
        fields = ('subcategory', 'avg_rate', 'category')
