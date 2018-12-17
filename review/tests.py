from datetime import timedelta as td

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

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

    def _post(self, data):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        return c.post("/api/v1/reviews/", data)

    def _run_and_assert_create(self, update, field, expected_message):
        data = self.REVIEW_PAYLOAD.copy()
        for key, value in update.items():
            if value is None:
                del data[key]
            else:
                data[key] = value

        response = self._post(data)

        self.assertEqual(response.status_code, 400)

        result = response.json()
        self.assertIn(field, result)
        self.assertIn(expected_message, result[field])

    def test_valid_create_and_list(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        object_count = Review.objects.count()

        r = c.post("/api/v1/reviews/", self.REVIEW_PAYLOAD)
        self.assertEqual(r.status_code, 201)

        review = Review.objects.get()
        self.assertEqual(Review.objects.count(), object_count + 1)
        self.assertEqual(review.summary, "ok")
        self.assertEqual(review.reviewer, self.user)
        self.assertAlmostEqual(review.created_at, timezone.now(), delta=td(seconds=2))

        r = c.get("/api/v1/reviews/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), object_count + 1)

    def test_not_authenticated_create(self):
        c = APIClient()
        r = c.post("/api/v1/reviews/", self.REVIEW_PAYLOAD)
        self.assertEqual(r.status_code, 401)

    def test_not_authenticated_list(self):
        c = APIClient()
        r = c.get("/api/v1/reviews/", self.REVIEW_PAYLOAD)
        self.assertEqual(r.status_code, 401)

    def test_create_w_missing_rating(self):
        self._run_and_assert_create({'rating': None}, "rating", "This field is required.")

    def test_create_w_invalid_rating(self):
        self._run_and_assert_create({'rating': -1}, "rating", "Ensure this value is greater than or equal to 1.")
        self._run_and_assert_create({'rating': 0}, "rating", "Ensure this value is greater than or equal to 1.")
        self._run_and_assert_create({'rating': 6}, "rating", "Ensure this value is less than or equal to 5.")
        self._run_and_assert_create({'rating': "very gut"}, "rating", "A valid integer is required.")

    def test_create_w_missing_title(self):
        self._run_and_assert_create({'title': None}, "title", "This field is required.")

    def test_create_w_invalid_title(self):
        self._run_and_assert_create({'title': ""}, "title", "This field may not be blank.")
        self._run_and_assert_create({'title': "a" * 65}, "title", "Ensure this field has no more than 64 characters.")

    def test_create_w_missing_summary(self):
        self._run_and_assert_create({'summary': None}, "summary", "This field is required.")

    def test_create_w_invalid_summary(self):
        self._run_and_assert_create({'summary': ""}, "summary", "This field may not be blank.")
        self._run_and_assert_create({'summary': "a" * 10001},
                                    "summary", "Ensure this field has no more than 10000 characters.")

    def test_create_w_missing_company(self):
        self._run_and_assert_create({'company_name': None}, "company_name", "This field is required.")
