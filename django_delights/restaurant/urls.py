from django.urls import path
from . import views

urlpatterns=[
    path('',views.Dashboard.as_view(), name="home"),
    path('/MenuItem/', views.Test.as_view(), name='menu_items'),
    path('/Inventory/', views.Test.as_view(), name='inventory'),
    path('/Purchases/', views.Test.as_view(), name='purchases'),
]