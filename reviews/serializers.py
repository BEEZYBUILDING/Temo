from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rating', 'title', 'body', 'created_at'
        ]
 
    def get_user(self, obj):
        return obj.user.full_name

class CreateReviewSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(required=False, allow_blank=True)
    order_id = serializers.IntegerField()