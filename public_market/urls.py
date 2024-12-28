# public/urls.py
from django.urls import path
from . import views
from .views import MultiStepFormView

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),  # Example path
    path('category_list/', views.category_list, name='category_list'),  # Add this line
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),  # Add this line
    path('for-sale/vehicles/', views.vehicles, name='vehicles'),  # Static route
    path('for-sale/<str:category_id>/', views.for_sale_category, name='for_sale_category'),
    path('services/', views.services_view, name='services'),
    # path('post-vehicle/', views.post_vehicle, name='post_vehicle'),
    # path('for-sale/vehicles/', views.vehicles, name='vehicles')




    # path('', Home.as_view(), name='home'),  # Home CBV
    # path('list/', ExperienceList.as_view(), name='experience-list'),  # Experience list view


    path('post/<str:category>/<int:step>/', MultiStepFormView.as_view(), name='post-item'),
    path('post/<str:category>/<int:step>/<int:item_id>/', MultiStepFormView.as_view(), name='post-item-edit'),

]

# <a href="{% url 'freelancer_profile:multi-step-edit' 0 %}">Freelancer Profile</a>


    # path('multi-step/<int:step>/', MultiStepFormView.as_view(), name='multi-step'),  # Multi-step form view
    # path('multi-step/<int:step>/<int:experience_id>/', MultiStepFormView.as_view(), name='multi-step-edit'),
    # path('delete/<int:pk>/', ExperienceDeleteView.as_view(), name='experience-delete'),  # Changed to pk