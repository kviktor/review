from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from review.models import Review


class ReviewTestCase(TestCase):
    REVIEW_PAYLOAD = {'rating': 5, 'title': "test", 'summary': "ok", 'company_name': "szia"}

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="test")
        cls.token = Token.objects.create(user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.token.delete()

    def test_create(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        r = c.post("/api/v1/reviews/", self.REVIEW_PAYLOAD)

        self.assertEqual(r.status_code, 201)
        review = Review.objects.get()
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.summary, "ok")
        self.assertEqual(review.reviewer, self.user)

    def test_not_authenticated_create(self):
        c = APIClient()
        r = c.post("/api/v1/reviews/", self.REVIEW_PAYLOAD)
        self.assertEqual(r.status_code, 401)
