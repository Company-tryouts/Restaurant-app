from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Food, Bookmark, Visited, Cuisine

class MyRestaurantTests(TestCase):
    fixtures = ["sample_data.json"]

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        from .models import Restaurant, Food
        self.restaurant = Restaurant.objects.first()
        self.food = Food.objects.filter(restaurant=self.restaurant).first()

    def test_restaurant_list_url(self):
        url = reverse('restaurants:restaurant_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)

    def test_restaurant_detail_url(self):
        url = reverse('restaurants:restaurant_detail', kwargs={'pk': self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)

    def test_restaurant_foods_url(self):
        url = reverse('restaurants:restaurant_foods', kwargs={'restaurant_id': self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.food.name)

    def test_toggle_bookmark_requires_login(self):
        url = reverse('restaurants:toggle_bookmark')
        response = self.client.post(url, {'restaurant_id': self.restaurant.id})
        self.assertEqual(response.status_code, 302) 

    def test_toggle_bookmark_logged_in(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('restaurants:toggle_bookmark')
        response = self.client.post(url, {'restaurant_id': self.restaurant.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(response.content, {'bookmarked': True})
        response = self.client.post(url, {'restaurant_id': self.restaurant.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(response.content, {'bookmarked': False})

    def test_toggle_visited_logged_in(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('restaurants:toggle_visited')
        response = self.client.post(url, {'restaurant_id': self.restaurant.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(response.content, {'visited': True})
        # Toggle again
        response = self.client.post(url, {'restaurant_id': self.restaurant.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(response.content, {'visited': False})
