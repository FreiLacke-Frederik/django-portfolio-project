from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView
from restaurant.models import Ingredient, MenuItem, Purchase
from restaurant.forms import MenuItemsUpdateForm, InventoryUpdateForm, PurchaseUpdateForm
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.urls import reverse
import json
import re

def authentication(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, "test.html")

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)

        purchases = Purchase.objects.all()

        purchase_amount = {}
        for purchase in Purchase.objects.all().select_related('item_name').values_list('item_name__menu_name', 'item_amount'):
            if purchase[0] not in purchase_amount.keys() and purchase[0] != None:
                purchase_amount[purchase[0]] = purchase[1]
            elif purchase[0] == None:
                pass
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
        inventory_value = round(inventory_value, 2)
        
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

def menu_item_update(request, pk):
    objects = MenuItem.objects.get(pk=pk)
    context = {"form": MenuItemsUpdateForm, "fields": objects, "pk": pk}
    
    if request.method == 'POST':
        query_dict_formatted = request.POST.copy()
        result = {"ingredients": {}}

        for i in range(0, len(temp:=re.split('\s+', query_dict_formatted["menu_ingredients"].strip().replace(":", ""))), 2):
            result["ingredients"][temp[i]] = temp[i+1] if not temp[i+1].endswith("g") else temp[i+1][:-1]

        query_dict_formatted["menu_ingredients"] = result

        form = MenuItemsUpdateForm(query_dict_formatted)

        if form.is_valid():
            for field_name, value in query_dict_formatted.items():
                setattr(objects, field_name, value)
            objects.save()

    return render(request, 'menu_item_update_form.html', context)

def menu_item_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    menu_item.delete()
    
    return redirect('menu_items')

def ingredient_update(request, pk):
    objects = Ingredient.objects.get(pk=pk)
    context = {"form": InventoryUpdateForm, "fields": objects, "pk": pk}

    if request.method == 'POST':
        form = InventoryUpdateForm(request.POST)

        if form.is_valid():
            for field_name, value in request.POST.items():
                setattr(objects, field_name, value)
            objects.save()

    return render(request, 'inventory_update_form.html', context)

def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    ingredient.delete()

    return redirect('inventory')

def purchase_update(request, pk):
    objects = Purchase.objects.get(pk=pk)
    context = {"form": PurchaseUpdateForm, "fields": objects, "pk": pk}

    if request.method == 'POST':
        form = PurchaseUpdateForm(request.POST)
        print("post")
        print(form)
        if form.is_valid():
            print("valid")
            for field_name, value in request.POST.items():
                if field_name != "item_name":
                    setattr(objects, field_name, value)
            objects.save()
    
    return render(request, 'purchase_update_form.html', context)

def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.delete()

    return redirect('purchases')