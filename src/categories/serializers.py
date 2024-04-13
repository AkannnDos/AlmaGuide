from rest_framework import serializers

from attractions.serializers import AttractionListSerializer
from categories.models import Category, Subcategory


class CategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.ImageField()


class CategoryRelatedSerializer(CategoryListSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, instance):
        request = self.context.get('request')
        if request:
            return getattr(instance, f'name_{request.LANGUAGE_CODE}')
        return instance.name_en


class SubcategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = CategoryRelatedSerializer()


class SubcategoryListSerializer(SubcategoriesSerializer):
    attractions = AttractionListSerializer(many=True)
