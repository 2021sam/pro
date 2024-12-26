# public/urls.py
from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),  # Example path
    path('category_list/', views.category_list, name='category_list'),  # Add this line
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),  # Add this line
    path('for-sale/<str:category_id>/', views.for_sale_category, name='for_sale_category'),
    path('services/', views.services_view, name='services'),
    path('post-vehicle/', views.post_vehicle, name='post_vehicle'),
    path('for-sale/vehicles/', views.vehicles, name='vehicles')
]
