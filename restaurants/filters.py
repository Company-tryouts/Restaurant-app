import django_filters
from django import forms
from .models import Restaurant, DietType, Cuisine
class RestaurantFilter(django_filters.FilterSet):

    cost_for_two_min = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="gte")
    cost_for_two_max = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="lte")

    diet_type = django_filters.MultipleChoiceFilter(
        choices=DietType.choices,
        widget=forms.CheckboxSelectMultiple
    )

    cuisines = django_filters.ModelMultipleChoiceFilter(
        queryset=Cuisine.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    rating = django_filters.MultipleChoiceFilter(
        field_name="average_rating",
        choices=[(n, n) for n in range(1, 6)],  # 1 to 5 stars
        lookup_expr="exact"
    )
    
    sort_by = django_filters.ChoiceFilter(
        method="filter_by_sort",
        choices=[
            ('price_low', 'Low → High'),
            ('price_high', 'High → Low'),
        ])

    class Meta:
        model = Restaurant
        fields = ['cost_for_two_min', 'cost_for_two_max', 'diet_type', 'cuisines', 'rating']

    def filter_by_sort(self, queryset, name, value):
        if value == "price_low":
            return queryset.order_by("cost_for_two")
        if value == "price_high":
            return queryset.order_by("-cost_for_two")
        return queryset
