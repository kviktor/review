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

        u2 = User.objects.create(username="test2")
        Review.objects.create(title="a", summary="b", rating=1, company_name="c", reviewer=u2)

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Token.objects.all().delete()
        Review.objects.all().delete()

    def _create_client(self, authenticate):
        client = APIClient()
        if authenticate:
            client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        return client

    def _post(self, url, data, authenticate=True):
        return self._create_client(authenticate).post(url, data, format="json")

    def _put(self, url, data, authenticate=True):
        return self._create_client(authenticate).put(url, data)

    def _get(self, url, authenticate=True):
        return self._create_client(authenticate).get(url)

    def _delete(self, url, authenticate=True):
        return self._create_client(authenticate).delete(url)

    def _run_and_assert_create(self, update, field, expected_message):
        data = self.REVIEW_PAYLOAD.copy()
        for key, value in update.items():
            if value is None:
                del data[key]
            else:
                data[key] = value

        response = self._post("/api/v1/reviews/", data)

        self.assertEqual(response.status_code, 400)

        result = response.json()
        self.assertIn(field, result)
        self.assertIn(expected_message, result[field])

    def test_valid_create_delete_update_retrieve_list(self):
        all_object_count = Review.objects.count()
        self_object_count = Review.objects.filter(reviewer=self.user).count()

        r = self._post("/api/v1/reviews/", self.REVIEW_PAYLOAD)
        self.assertEqual(r.status_code, 201)

        review = Review.objects.latest("created_at")
        self.assertEqual(Review.objects.count(), all_object_count + 1)
        self.assertEqual(review.summary, "ok")
        self.assertEqual(review.reviewer, self.user)
        self.assertEqual(review.ip_address, "127.0.0.1")
        self.assertAlmostEqual(review.created_at, timezone.now(), delta=td(seconds=2))

        review_id = r.json()['id']
        response = self._delete(f"/api/v1/reviews/{review_id}/")
        self.assertEqual(response.status_code, 405)

        data = self.REVIEW_PAYLOAD.copy()
        data['title'] = "different title"
        response = self._put(f"/api/v1/reviews/{review_id}/", data)
        self.assertEqual(response.status_code, 405)

        response = self._get(f"/api/v1/reviews/{review_id}/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.summary, data['summary'])
        self.assertEqual(review.rating, data['rating'])
        self.assertEqual(review.title, data['title'])
        self.assertEqual(review.reviewer.username, data['reviewer'])

        response = self._get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self_object_count + 1)

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

    def test_not_authenticated_create(self):
        r = self._post("/api/v1/reviews/", self.REVIEW_PAYLOAD, authenticate=False)
        self.assertEqual(r.status_code, 401)

    def test_not_authenticated_list(self):
        r = self._get("/api/v1/reviews/", authenticate=False)
        self.assertEqual(r.status_code, 401)

    def test_not_authenticated_retrieve(self):
        review = Review.objects.latest("created_at")
        r = self._get(f"/api/v1/reviews/{review.id}/", authenticate=False)
        self.assertEqual(r.status_code, 401)

    def test_not_existing_retrieve(self):
        r = self._get(f"/api/v1/reviews/12345/")
        self.assertEqual(r.status_code, 404)

    def test_not_authorized_retrieve(self):
        review = Review.objects.latest("created_at")
        r = self._get(f"/api/v1/reviews/{review.id}/")
        self.assertEqual(r.status_code, 403)

    def test_list_wo_reviews(self):
        resp = self._get(f"/api/v1/reviews/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 0)

    def test_review_model_str(self):
        review = Review.objects.latest("created_at")
        self.assertEqual(
            str(review),
            f"{review.rating} - {review.title} - {review.company_name} - {review.reviewer.username}"
        )
