from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.Dashboard.as_view(), name="home"),
    path('menu-items/', views.Test.as_view(), name='menu_items'),
    path('inventory/', views.Test.as_view(), name='inventory'),
    path('purchases/', views.Test.as_view(), name='purchases'),
    path('__reload__/', include("django_browser_reload.urls"))
]