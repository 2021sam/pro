from django.urls import path
from . import views

app_name = 'skill'
urlpatterns = [
    path('skill/', views.home, name='skill'),
    path('skill/view/', views.view, name='skill-view'),
    # path('skill/view/summarize/', views.view_summarize, name='skill-summarize'),
    path('skill/add/', views.add, name='skill-add'),
    path('skill/edit/', views.edit, name='skill-edit'),
    path('skill/edithx/', views.edit_hx, name='skill-edit-hx'),
    path('skill/delete/<int:id>/', views.delete, name='skill-delete'),
    path('skill/hx/delete/<int:id>/', views.hx_delete, name='hx-skill-delete'),
    path('skill/hx/put/<int:id>/', views.hx_put, name='hx-skill-put'),
    path('skill/hx/post/<int:id>/', views.hx_post, name='hx-skill-post'),
    path('skill/hx/', views.hx, name='hx'),
    path('skill/hx2/', views.hx2, name='hx2')
]
