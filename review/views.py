from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from review.models import Review
from review.serializers import ReviewSerializer
from review.permissions import IsReviewer
from review.utils import get_ip_address_from_request


class ReviewList(ListCreateAPIView):
    """
    get:
    List all reviews submitted by the user.

    post:
    Create a new review.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        ip_address = get_ip_address_from_request(self.request)
        serializer.save(reviewer=self.request.user, ip_address=ip_address)

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)


class ReviewDetail(RetrieveAPIView):
    """
    Retrieve a single review
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsReviewer)
