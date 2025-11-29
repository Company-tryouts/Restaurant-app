from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Bookmark, Visited, Cuisine
from decimal import Decimal
from datetime import time

class RestaurantViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Test City",
            address="123 Test St",
            cost_for_two=500,
            diet_type=1,
            average_rating=0.0,
            opening_time=time(10, 0),
            closing_time=time(22, 0)
        )
        self.restaurant.cuisines.add(self.cuisine)
        self.restaurant.save()
        
    def test_restaurant_list_view(self):
        url = reverse("restaurants:restaurant_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)
        
    def test_restaurant_detail_view(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.restaurant.address)
    
    def test_food_list_view(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)
    
    def test_toggle_bookmark_requires_login(self):
        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.pk})
        self.assertEqual(response.status_code, 302)  # redirects to login
    
    def test_toggle_bookmark_creates_and_deletes(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("restaurants:toggle_bookmark")
        
        response = self.client.post(url, {"restaurant_id": self.restaurant.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"bookmarked": True})
        
        response = self.client.post(url, {"restaurant_id": self.restaurant.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"bookmarked": False})
    
    def test_toggle_visited_requires_login(self):
        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.pk})
        self.assertEqual(response.status_code, 302)  # redirect to login
    
    def test_toggle_visited_creates_and_deletes(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("restaurants:toggle_visited")
        
        # Create visited
        response = self.client.post(url, {"restaurant_id": self.restaurant.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"visited": True})
        
        response = self.client.post(url, {"restaurant_id": self.restaurant.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"visited": False})
