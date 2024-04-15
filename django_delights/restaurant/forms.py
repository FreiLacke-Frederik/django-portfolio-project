from django import forms
from .models import MenuItem, Purchase, Ingredient

class MenuItemsUpdateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ("menu_name", "menu_price", "menu_ingredients")