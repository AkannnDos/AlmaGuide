from rest_framework import serializers


class TourSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    price = serializers.IntegerField()
    duration = serializers.IntegerField()
    avg_rate = serializers.DecimalField(max_digits=3, decimal_places=2)
    way_to_travel = serializers.CharField()
