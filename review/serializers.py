from rest_framework.serializers import ModelSerializer

from review.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "rating", "title", "summary", "created_at", "company_name", "reviewer")
