import json
from pathlib import Path
from django.http import JsonResponse

BASE_DIR = Path(__file__).resolve().parent.parent

def load_json_data(filename):
    """Utility function to load JSON data from the data folder."""
    file_path = BASE_DIR / "public_market" / "data" / filename
    with open(file_path, "r") as file:
        return json.load(file)

def for_sale_view(request):
    """View to return categories for items for sale."""
    for_sale = load_json_data("for_sale.json")
    return JsonResponse(for_sale)

def services_view(request):
    """View to return services."""
    services = load_json_data("services.json")
    return JsonResponse(services)





# # public_market/views.py
from django.http import HttpResponse
from django.shortcuts import render



# import json
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# def load_json_data(filename):
#     file_path = BASE_DIR / "public_market" / "data" / filename
#     with open(file_path, "r") as file:
#         return json.load(file)

# items_for_sale = load_json_data("items_for_sale.json")
# services = load_json_data("services.json")



def index(request):
    # return HttpResponse("Welcome to Public Market!")
    return render(request, 'public_market/index.html')


def category_list(request):
    return HttpResponse("Category List")


def item_detail(request, item_id):
    return HttpResponse(f"Item Detail for item_id: {item_id}")
