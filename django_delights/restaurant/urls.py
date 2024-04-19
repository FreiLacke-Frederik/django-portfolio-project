from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.Dashboard.as_view(), name="home"),
    path('menu-items/', views.MenuItemsList.as_view(), name='menu_items'),
    path('menu-items/<int:pk>', views.menu_item_update, name='menu_items_update'),
    path('menu-items/delete/<int:pk>', views.menu_item_delete, name='menu_item_delete'),
    path('inventory/', views.InventoryList.as_view(), name='inventory'),
    path('purchases/', views.PurchaseList.as_view(), name='purchases'),
    path('__reload__/', include("django_browser_reload.urls")),
]