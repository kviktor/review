from rest_framework.serializers import ModelSerializer, ReadOnlyField

from review.models import Review


class ReviewSerializer(ModelSerializer):
    reviewer = ReadOnlyField(source="reviewer.username")

    class Meta:
        model = Review
        fields = ("id", "rating", "title", "summary", "created_at", "company_name", "reviewer", )
