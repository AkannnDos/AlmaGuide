from rest_framework import serializers

from attractions.serializers import AttractionListSerializer
from categories.models import Category, Subcategory


class SubcategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    attractions = AttractionListSerializer(many=True)
