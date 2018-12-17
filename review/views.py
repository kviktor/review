from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from review.models import Review
from review.serializers import ReviewSerializer


class ReviewList(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
