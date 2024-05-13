from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView
from restaurant.models import Ingredient, MenuItem, Purchase
from restaurant.forms import MenuItemsUpdateForm, MenuItemsCreateForm, InventoryUpdateForm, InventoryCreateForm, PurchaseUpdateForm, PurchaseCreateForm
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
        context["columns"] = ["Amount", "Menu", "Price", "Time"]

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

def menu_item_create(request):

    if request.method == 'POST':
        query_dict_formatted = request.POST.copy()
        result = {"ingredients": {}}

        for i in range(0, len(temp:=re.split('\s+', request.POST["menu_ingredients"].strip().replace(":", ""))), 2):
            result["ingredients"][temp[i]] = temp[i+1] if not temp[i+1].endswith("g") else temp[i+1][:-1]

        query_dict_formatted["menu_ingredients"] = result
        
        form = MenuItemsCreateForm(query_dict_formatted)

        if form.is_valid():
            new_data = {}
            for key in query_dict_formatted:
                if key != "csrfmiddlewaretoken":
                    new_data[key] = query_dict_formatted[key]
            
            new_entry = MenuItem.objects.create(**new_data)

            return redirect('menu_items')
        
    return render(request, 'menu_item_create.html')

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

def ingredient_create(request):

    if request.method == 'POST':
        form = InventoryCreateForm(request.POST)
        
        if form.is_valid():
            queryset_formatted = {obj: request.POST[obj] for obj in request.POST if obj != "csrfmiddlewaretoken"}
            new_entry = Ingredient.objects.create(**queryset_formatted)

            return redirect('inventory')
        else:
            print("Invalid form")
    return render(request, 'inventory_create.html')

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

def purchase_create(request):
    menus = MenuItem.objects.values("menu_name", "pk")
    context = {"menus": menus}

    if request.method == 'POST':
        form = PurchaseCreateForm(request.POST)
        
        if form.is_valid():
            selected_menu_id = request.POST.get("item_name")
            amount_purchased = request.POST.get("item_amount")
            menu_item = MenuItem.objects.get(pk=selected_menu_id)
            menu_ingredients = menu_item.menu_ingredients
            purchase_legitimate = True
            
            for ingredient, ingredient_amount in menu_ingredients["ingredients"].items():
                if not Ingredient.objects.get(ingredient_name=ingredient).ingredient_amount >= float(ingredient_amount):
                    purchase_legitimate = False
                    break
            
            if purchase_legitimate:
                queryset_formatted = {obj: request.POST[obj] for obj in request.POST if obj != "csrfmiddlewaretoken"}
                queryset_formatted["item_name"] = MenuItem.objects.get(pk=queryset_formatted["item_name"])
                queryset_formatted["purchase_time"] = datetime.now()
                new_entry = Purchase.objects.create(**queryset_formatted)

                for ingredient, ingredient_amount in menu_ingredients["ingredients"].items():
                    inventory_ingredient = Ingredient.objects.get(ingredient_name=ingredient)
                    inventory_ingredient.ingredient_amount -= (float(ingredient_amount)*float(amount_purchased))
                    inventory_ingredient.save()

                return redirect('purchases')
            
            elif not purchase_legitimate:
                print("Insert code here to notify user that purchase could no be added due to low ingredients")

    return render(request, 'purchase_create.html', context)