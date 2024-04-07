from rest_framework import serializers

from utils.choices import ValueChoices


class AttractionListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()
    distance = serializers.SerializerMethodField()
    category_icon = serializers.ImageField()
    avg_rate = serializers.DecimalField(max_digits=3, decimal_places=2)

    def get_distance(self, instance):
        return str(instance.distance.m)
    

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
