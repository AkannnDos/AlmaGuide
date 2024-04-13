from django_filters import rest_framework as filters


from categories.models import Subcategory

class SubcategoryFilterSet(filters.FilterSet):

    class Meta:
        model = Subcategory
        fields = ('category', )
