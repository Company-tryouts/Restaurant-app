from django.contrib.auth.models import User
from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
DIET_VEG = 1
DIET_NONVEG = 2
DIET_VEGAN = 3

DIET_CHOICES = [
    (DIET_VEG, 'Vegetarian'),
    (DIET_NONVEG, 'Non-Vegetarian'),
    (DIET_VEGAN, 'Vegan'),
]

class Restaurant(models.Model):


    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    cost_for_two = models.IntegerField()
    diet_type = models.IntegerField(choices=DIET_CHOICES)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_spotlight = models.BooleanField(default=False)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')

    def __str__(self):
        return self.name


class Food(models.Model):


    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    diet_type = models.IntegerField(choices=DIET_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    
class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="restaurant_images/")



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        abstract = True



class Review(models.Model, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # ensures one review per user per restaurant

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} - {self.rating}"




class Bookmark(models.Model, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookmarked_by')

    class Meta:
        unique_together = ('user', 'restaurant')  # ensures no duplicate bookmarks

    def __str__(self):
        return f"{self.user.username} bookmarked {self.restaurant.name}"




class Visited(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visited_restaurants')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='visited_by')
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # ensures one visit per user per restaurant

    def __str__(self):
        return f"{self.user.username} visited {self.restaurant.name}"




