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



# def index(request):
#     # return HttpResponse("Welcome to Public Market!")
#     return render(request, 'public_market/index.html')


def category_list(request):
    return HttpResponse("Category List")


def item_detail(request, item_id):
    return HttpResponse(f"Item Detail for item_id: {item_id}")





# import json
# from django.shortcuts import render
# import os

# def index(request):
#     # Get the path to the data directory
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     json_file_path = os.path.join(base_dir, 'public_market', 'data', 'for_sale.json')
    
#     # Load categories from the JSON file
#     with open(json_file_path, 'r') as file:
#         data = json.load(file)
    
#     categories = data.get("categories", [])  # Fetch categories from JSON
#     print(categories)


#     return render(request, 'public_market/index.html', {'categories': categories})




from django.shortcuts import render
import json
from pathlib import Path

def index(request):
    # Load data from the JSON file
    data_path = Path(__file__).resolve().parent / "data" / "for_sale.json"
    with open(data_path, "r") as file:
        categories_data = json.load(file)
    
    # Prepare categories with id and name
    categories = [
        {"id": category["id"], "name": category["name"], "description": category.get("description", "")}
        for category in categories_data
    ]
    
    return render(request, "public_market/index.html", {"categories": categories})
