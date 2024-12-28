import json
from pathlib import Path
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

# Load CATEGORY_CONFIG from config.json
CATEGORY_CONFIG = load_json_data("config.json")




# # public_market/views.py
from django.http import HttpResponse
from django.shortcuts import render

def category_list(request):
    return HttpResponse("Category List")


def item_detail(request, item_id):
    return HttpResponse(f"Item Detail for item_id: {item_id}")


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



from django.shortcuts import render, redirect
from .forms import VehicleListingForm

@login_required
def post_vehicle(request):
    if request.method == 'POST':
        form = VehicleListingForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            # return redirect('public:vehicles')  # Redirect to the list of vehicles
            return redirect('/public/for-sale/vehicles/')  # Use the absolute path here
    else:
        form = VehicleListingForm()

    return render(request, 'public_market/post_vehicle.html', {'form': form})


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















# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
# from .config import CATEGORY_CONFIG
# CATEGORY_CONFIG = load_json_data("config.json")


@method_decorator(login_required, name='dispatch')
class MultiStepFormView(View):
    # def get_category_config(self, category):
    #     """Retrieve category-specific config or default config."""
    #     return CATEGORY_CONFIG.get(category, CATEGORY_CONFIG['default'])

    def get(self, request, category, step=0, item_id=None):
        category_key = category
        print('MultiStepFormView - get')
        """Handle GET requests to display forms."""
        category_config = load_json_data("config.json")
        category  = category_config[category]
        print(category)

        # category_config = self.get_category_config(category)
        form_class = category['forms'][step]
        template = category['templates'][step]
        model = category['model']
        print(f'form_class: {form_class}')
        print(f'template: {template}')
        print(f'model: {model}')
        # If editing, fetch the item; else, initialize a blank form
        item = get_object_or_404(category['model'], pk=item_id) if item_id else None
        form = form_class(instance=item)

        return render(request, template, {
            'form': form,
            'step': step,
            'total_steps': len(category['forms']),
            'item_id': item_id,
            'category': category_key,
        })

    def post(self, request, category, step=0, item_id=None):
        """Handle POST requests to save forms."""
        category_config = self.get_category_config(category)
        form_class = category_config['forms'][step]

        # If editing, fetch the item; else, initialize a blank form
        item = get_object_or_404(category_config['model'], pk=item_id) if item_id else None
        form = form_class(request.POST, instance=item)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user  # Set the user if necessary
            item.save()

            # Proceed to the next step or finish
            next_step = step + 1
            if next_step < len(category_config['forms']):
                return redirect('post-item', category=category, step=next_step, item_id=item.id)
            return redirect('item-list')  # Adjust to your final redirection

        # Re-render the current step with errors
        return render(request, category_config['templates'][step], {
            'form': form,
            'step': step,
            'total_steps': len(category_config['forms']),
            'item_id': item_id,
            'category': category,
        })

