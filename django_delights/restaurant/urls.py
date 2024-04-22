from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.authentication, name='authentication'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('menu-items/', views.MenuItemsList.as_view(), name='menu_items'),
    path('menu-items/<int:pk>', views.menu_item_update, name='menu_items_update'),
    path('menu-items/delete/<int:pk>', views.menu_item_delete, name='menu_item_delete'),
    path('inventory/', views.InventoryList.as_view(), name='inventory'),
    path('ingredients/<int:pk>', views.ingredient_update, name='ingredient_update'),
    path('ingredients/delete/<int:pk>', views.ingredient_delete, name='ingredient_delete'),
    path('purchases/', views.PurchaseList.as_view(), name='purchases'),
    path('purchases/<int:pk>', views.purchase_update, name='purchase_update'),
    path('purchases/delete/<int:pk>', views.purchase_delete, name='purchase_delete'),
    path('__reload__/', include("django_browser_reload.urls")),
]