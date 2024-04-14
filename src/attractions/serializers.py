from rest_framework import serializers

from attractions.models import ChoseAttraction

from utils.choices import ValueChoices


class AttractionListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()
    name = serializers.CharField()
    distance = serializers.SerializerMethodField()
    category_icon = serializers.SerializerMethodField()
    avg_rate = serializers.DecimalField(max_digits=3, decimal_places=2)

    def get_distance(self, instance):
        return str(instance.distance.m)
    
    def get_category_icon(self, instance):
        if instance.subcategory.category.icon:
            request = self.context.get('request')
            icon_url = instance.subcategory.category.icon.url
            return request.build_absolute_uri(icon_url)
        return None
    

class DetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()
    value_type = serializers.ChoiceField(
        choices=ValueChoices.choices
    )
    

class AttractionDetailSerializer(AttractionListSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    details = DetailSerializer(many=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    def get_latitude(self, instance):
        return str(instance.location.coords[0])
        
    def get_longitude(self, instance):
        return str(instance.location.coords[1])


class ChosenAttractionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChoseAttraction
        fields = ('attraction', 'id')


class MakeRouteSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()


class RouteListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class YandexResponseSerializer(serializers.Serializer):
    url = serializers.URLField()
