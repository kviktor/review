from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from review.models import Review


class ReviewTestCase(TestCase):
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

        req = {'rating': 5, 'title': "test", 'summary': "ok", 'company_name': "szia", 'reviewer': 1}
        r = c.post("/api/v1/reviews/", req)

        self.assertEqual(r.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().summary, "ok")
