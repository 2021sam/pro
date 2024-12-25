# public_market/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Public Market!")


# public_market/views.py
from django.http import HttpResponse

def category_list(request):
    return HttpResponse("Category List")

# public_market/views.py
from django.http import HttpResponse

def item_detail(request, item_id):
    return HttpResponse(f"Item Detail for item_id: {item_id}")
