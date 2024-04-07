from rest_framework import serializers

from reviews.models import AttractionReview, TourReview
from users.serializers import UserSerializer


class ReviewRetrieveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    rate = serializers.IntegerField()
    review = serializers.CharField()
    user = UserSerializer()


class AttractionReviewCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AttractionReview
        fields = (
            'rate', 'review', 'attraction'
        )
    

class TourReviewCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TourReview
        fields = (
            'rate', 'review', 'tour'
        )
