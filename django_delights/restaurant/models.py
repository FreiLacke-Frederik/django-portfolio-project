from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import activate
from datetime import datetime

class MenuItem(models.Model):
    menu_name = models.CharField(max_length=100)
    menu_price = models.FloatField(default=0)
    menu_ingredients = models.JSONField(default=0, null=True)

    def __str__(self):
        return self.menu_name

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ("g", "Gramm")
    ]

    ingredient_name = models.CharField(max_length=100)
    ingredient_amount = models.FloatField(default=0)
    ingredient_unit = models.CharField(max_length=30, choices=UNIT_CHOICES)
    price_per_kilo = models.FloatField(default=0, null=True)

    def __str__(self) -> str:
        return f"{self.ingredient_name} - {self.ingredient_amount}{self.ingredient_unit} ({self.ingredient_amount/1000}kg)"
    

class Purchase(models.Model):  
    item_amount = models.IntegerField(default=0)
    item_name = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    item_price = models.FloatField(default=0, null=True, blank=True)
    purchase_time = models.DateTimeField()

    def __str__(self):
        return f"{self.item_amount}x {self.item_name} - {self.item_price}€"