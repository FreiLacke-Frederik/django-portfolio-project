from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from restaurant.models import Ingredient, MenuItem, Purchase
from django.db.models import Sum
 
class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        purchases = Purchase.objects.all()

        purchase_amount = {}
        for purchase in Purchase.objects.all().select_related('item_name').values_list('item_name__menu_name', 'item_amount'):
            if purchase[0] not in purchase_amount.keys():
                purchase_amount[purchase[0]] = purchase[1]
            else:
                purchase_amount[purchase[0]] += purchase[1]

        top_three_sales = sorted(purchase_amount.items(), key=lambda x: x[1], reverse=True)[:3]
        revenue = round(Purchase.objects.aggregate(revenue=Sum("price"))["revenue"], 4)

        low_ingredients = {}
        for ingredient in Ingredient.objects.order_by("ingredient_amount").values_list("ingredient_name", "ingredient_amount"):
            if ingredient[1] < 500:
                low_ingredients[ingredient[0]] = ingredient[1]

        context["top_three_sales"] = top_three_sales
        context["revenue"] = revenue
        context["low_stock_items"] = low_ingredients
        return context

class Test(TemplateView):
    template_name = "test.html"