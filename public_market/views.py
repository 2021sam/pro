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

# def index(request):
#     # Load data from the JSON file
#     data_path = Path(__file__).resolve().parent / "data" / "for_sale.json"
#     with open(data_path, "r") as file:
#         categories_data = json.load(file)
    
#     # Prepare categories with id and name
#     categories = [
#         {"id": category["id"], "name": category["name"], "description": category.get("description", "")}
#         for category in categories_data
#     ]
    
#     return render(request, "public_market/index.html", {"categories": categories})

# from django.shortcuts import render
# import os
# import json

# def index(request):
#     # Load categories from the JSON file
#     data_file = os.path.join(os.path.dirname(__file__), 'data', 'for_sale.json')
#     with open(data_file, 'r') as file:
#         data = json.load(file)

#     # Pass the categories to the template
#     return render(request, 'public_market/index.html', {"categories": data.get("categories", [])})

from django.shortcuts import render
import os
import json

def index(request):
    # Load categories from the JSON file
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'for_sale.json')
    with open(data_file, 'r') as file:
        data = json.load(file)  # Assuming data is a list of categories

    # Pass the categories to the template
    return render(request, 'public_market/index.html', {"categories": data})



from django.shortcuts import render
import os
import json

def category_detail(request, category):
    # Load categories from the JSON file
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'for_sale.json')
    with open(data_file, 'r') as file:
        data = json.load(file)

    # Check if the category exists
    categories = data.get("categories", [])
    if category not in categories:
        return render(request, 'public_market/404.html', {"message": "Category not found"}, status=404)

    # Pass the category name to the template
    return render(request, 'public_market/category_detail.html', {"category_name": category})


# from django.shortcuts import render
# import os
# import json

# def for_sale_category(request, category_id):
#     print('............................................')
#     # Load categories from JSON
#     data_file = os.path.join(os.path.dirname(__file__), 'data', 'for_sale.json')
#     with open(data_file, 'r') as file:
#         categories = json.load(file)

#     # Match the requested category ID
#     category = next((cat for cat in categories if cat['id'] == category_id), None)
#     print('*******************************')
#     print(category)

#     if not category:
#         return render(request, '404.html', status=404)

#     print('for_sale_category')
#     return render(request, 'public_market/for_sale_category.html', {"category": category})




from django.shortcuts import render, get_object_or_404
from .models import VehicleListing  # Add other category-specific models as needed

def for_sale_category(request, category_id):
    if category_id == "vehicles":
        items = VehicleListing.objects.all()
        category_name = "Vehicles"
    else:
        items = []  # Add logic for other categories here
        category_name = category_id.capitalize()  # Placeholder, adjust as needed

    return render(
        request, 
        'public_market/for_sale_category.html', 
        {"category": {"name": category_name, "items": items}}
    )




# pro/public_market/views.py

from django.shortcuts import render, redirect
from .forms import VehicleListingForm

def post_vehicle(request):
    if request.method == 'POST':
        form = VehicleListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('public:index')  # Redirect to homepage or another success page
    else:
        form = VehicleListingForm()

    return render(request, 'public_market/post_vehicle.html', {'form': form})




# from django.shortcuts import render
# from public_market.models import VehicleListing

# def vehicles(request):
#     vehicle_listings = VehicleListing.objects.all()  # Fetch all vehicle listings
#     return render(
#         request, 
#         'public_market/for_sale_category.html', 
#         {"category": {"name": "Vehicles", "items": vehicle_listings}}
#     )




from django.shortcuts import render
from public_market.models import VehicleListing

def vehicles(request):
    vehicle_listings = VehicleListing.objects.all()  # Fetch all vehicle ads
    print(vehicle_listings)  # Debug: Print the queryset to verify
    for vehicle in vehicle_listings:
        print(vehicle.title, vehicle.price, vehicle.description)  # Ensure all data is present
    return render(
        request, 
        'public_market/for_sale_category.html', 
        {"category": {"name": "Vehicles", "items": vehicle_listings}}
    )
