from django import forms
from .models import MenuItem, Purchase, Ingredient

class MenuItemsUpdateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"

class MenuItemsCreateForm(forms.ModelForm):
    class Meta: 
        model = MenuItem
        fields = "__all__"

class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"

class PurchaseUpdateForm(forms.ModelForm):
    class Meta: 
        model = Purchase
        fields = ["item_amount", "price"]