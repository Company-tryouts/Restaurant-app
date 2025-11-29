from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Cuisine, Food, Bookmark, Visited
import datetime

class UserMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass123")
        super().setUpTestData()

    def login(self):
        self.client.login(username="testuser", password="pass123")


class RestaurantMixin(UserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.cuisine = Cuisine.objects.create(name="Indian")
        cls.restaurant = Restaurant.objects.create(
            name="Burger King",
            address="Street 1",
            diet_type=1,
            average_rating=4.5,
            cost_for_two=400,
            opening_time=datetime.time(9, 0),   
            closing_time=datetime.time(22, 0)
        )
        cls.restaurant.cuisines.add(cls.cuisine)


class FoodMixin(RestaurantMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.food = Food.objects.create(
            restaurant=cls.restaurant,
            name="Fried Rice",
            price=150,
            diet_type=1
        )


# ------ TESTS ------

class TestRestaurantListView(RestaurantMixin):
    def test_list_page_should_load_restaurants(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")

    def test_restaurant_list_should_filter_by_price_range(self):

        response = self.client.get(reverse("restaurants:restaurant_list") + "?max_price=500")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")
        self.assertNotContains(response, "Fancy Feast")



class TestRestaurantDetailView(RestaurantMixin):
    def test_detail_page_should_display_correct_restaurant(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")


class TestFoodListView(FoodMixin):
    def test_food_list_should_show_related_food(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fried Rice")


class TestToggleBookmark(RestaurantMixin):
    def test_user_should_toggle_bookmark(self):
        self.login()
        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists()
        )


class TestToggleVisited(RestaurantMixin):
    def test_user_should_toggle_visited_status(self):
        self.login()
        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists()
        )
