from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Food, Bookmark, Visited, Cuisine
from datetime import time

@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher']
)
class MyRestaurantTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="StrongPassword123!"
        )

        cls.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="TestCity",
            address="Somewhere",
            cost_for_two=500,
            opening_time=time(9, 0),
            closing_time=time(22, 0),
        )

        cls.cuisine = Cuisine.objects.create(name="South Indian")
        cls.restaurant.cuisines.add(cls.cuisine)

        cls.food = Food.objects.create(
            restaurant=cls.restaurant,
            name="Masala Dosa",
            price=120
        )

    def test_restaurant_list_url(self):
        url = reverse("restaurants:restaurant_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")

    def test_restaurant_detail_url(self):
        url = reverse("restaurants:restaurant_detail", args=[self.restaurant.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)

    def test_restaurant_foods_url(self):
        url = reverse("restaurants:restaurant_foods", args=[self.restaurant.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.food.name)

    def test_toggle_bookmark_requires_login(self):
        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 302)

    def test_toggle_bookmark_logged_in(self):
        self.client.login(username="testuser", password="StrongPassword123!")
        url = reverse("restaurants:toggle_bookmark")

        response = self.client.post(url, {"restaurant_id": self.restaurant.id}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertJSONEqual(response.content, {"bookmarked": True})

        response = self.client.post(url, {"restaurant_id": self.restaurant.id}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertJSONEqual(response.content, {"bookmarked": False})

    def test_toggle_visited_logged_in(self):
        self.client.login(username="testuser", password="StrongPassword123!")
        url = reverse("restaurants:toggle_visited")

        response = self.client.post(url, {"restaurant_id": self.restaurant.id}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertJSONEqual(response.content, {"visited": True})

        response = self.client.post(url, {"restaurant_id": self.restaurant.id}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertJSONEqual(response.content, {"visited": False})
