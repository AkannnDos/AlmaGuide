from rest_framework import serializers


class ExchangeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    currency = serializers.CharField()
    rate = serializers.DecimalField(max_digits=100, decimal_places=2)
