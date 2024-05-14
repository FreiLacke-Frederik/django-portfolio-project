from django import forms
from .models import MenuItem, Purchase, Ingredient

class MenuItemsUpdateForm(forms.ModelForm):
    menu_name = forms.CharField(required=True)  
    menu_price = forms.FloatField(required=True)  
    menu_ingredients = forms.JSONField(required=True)  
    
    class Meta:
        model = MenuItem
        fields = "__all__"

class MenuItemsCreateForm(forms.ModelForm):
    menu_name = forms.CharField(required=True)  
    menu_price = forms.FloatField(required=True)  
    menu_ingredients = forms.JSONField(required=True)  

    class Meta: 
        model = MenuItem
        fields = "__all__"

class InventoryUpdateForm(forms.ModelForm):
    ingredient_name = forms.CharField(required=True)  
    ingredient_amount = forms.FloatField(required=True)  
    ingredient_unit = forms.CharField(required=True)  
    price_per_kilo = forms.FloatField(required=True)  

    class Meta:
        model = Ingredient
        fields = "__all__"

class InventoryCreateForm(forms.ModelForm):
    ingredient_name = forms.CharField(required=True)  
    ingredient_amount = forms.FloatField(required=True)  
    ingredient_unit = forms.CharField(required=True)  
    price_per_kilo = forms.FloatField(required=True)  

    class Meta:
        model = Ingredient
        fields = "__all__"

class PurchaseUpdateForm(forms.ModelForm):
    item_amount = forms.IntegerField(required=True)  
    item_name = forms.ModelChoiceField(queryset=MenuItem.objects.all(), required=True)  
    price = forms.FloatField(required=True) 

    class Meta: 
        model = Purchase
        fields = ["item_amount", "price"]

class PurchaseCreateForm(forms.ModelForm):
    item_amount = forms.IntegerField(required=True)  
    item_name = forms.ModelChoiceField(queryset=MenuItem.objects.all(), required=True)  
    price = forms.FloatField(required=True)  
    
    class Meta:
        model = Purchase
        fields = ["item_amount", "item_name", "price"]
