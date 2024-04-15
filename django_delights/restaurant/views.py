from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView
from restaurant.models import Ingredient, MenuItem, Purchase
from restaurant.forms import MenuItemsUpdateForm
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import datetime
 
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
        sales_count = Purchase.objects.count()

        low_ingredients = {}
        for ingredient in Ingredient.objects.order_by("ingredient_amount").values_list("ingredient_name", "ingredient_amount"):
            if ingredient[1] < 500:
                low_ingredients[ingredient[0]] = ingredient[1]
        
        inventory_value = 0
        for row in Ingredient.objects.values_list("ingredient_amount", "price_per_kilo"):
            inventory_value += (row[0]*row[1])/1000

        sales = Purchase.objects.annotate(tag=TruncDate('purchase_time')).values('tag').annotate(gesamtkäufe=Count('id')).order_by('tag')
        sales_per_day = [[datetime.strftime(sale["tag"], "%d. %B") for sale in sales], [sale["gesamtkäufe"] for sale in sales]]

        context["top_three_sales"] = top_three_sales
        context["revenue"] = revenue
        context["low_stock_items"] = low_ingredients
        context["sales_count"] = sales_count
        context["inventory_value"] = inventory_value
        context["sales_per_day"] = sales_per_day
        return context

class MenuItemsList(TemplateView):
    template_name = "menu_item_table.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        menu_items = MenuItem.objects.all()

        context["data"] = menu_items
        context["columns"] = ["Name", "Price", "Ingredients"]

        return context
    
class InventoryList(TemplateView):
    template_name = "inventory_table.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        inventory_items = Ingredient.objects.all()

        context["data"] = inventory_items
        context["columns"] = ["Name", "Amount", "Unit", "Price per Kilo"]

        return context
    
class PurchaseList(TemplateView):
    template_name = "purchase_table.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        purchases = Purchase.objects.all()

        context["data"] = purchases
        context["columns"] = ["Amount", "Name", "Price", "Time"]

        return context

class MenuItemUpdate(UpdateView):
    template_name = 'menu_item_update_form.html'
    model = MenuItem
    form_class = MenuItemsUpdateForm