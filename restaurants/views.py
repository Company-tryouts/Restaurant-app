from django.shortcuts import render
from .models import Restaurant, Food, Cuisine
from django.views.generic import ListView, DetailView

# Create your views here.

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurants/list.html"  
    context_object_name = "restaurants"  
    paginate_by = 10  

    ordering = ['-average_rating']

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images')  # fetch images to avoid extra queries
        return qs

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/detail.html"  
    context_object_name = "restaurant"

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images', 'cuisines')
    
class FoodListView(ListView):
    model = Food
    template_name = "foods/list.html"
    context_object_name = "foods"

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Food.objects.filter(restaurant_id=restaurant_id).prefetch_related('cuisines')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_id = self.kwargs.get('restaurant_id')
        context['restaurant'] = Restaurant.objects.get(id=restaurant_id)
        return context

