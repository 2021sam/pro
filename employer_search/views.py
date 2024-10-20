from django.shortcuts import render
from .forms import FreelancerSearchForm  # Assuming a form for entering job zip code and commute limit
from freelancer_profile.models import FreelancerProfile
from geopy.distance import geodesic  # For calculating distances between zip codes  pip install geopy
from django.http import HttpResponseRedirect
from django.urls import reverse

def search_freelancers(request):
    """ View to handle recruiter search form input (job zip code and commute limit) """
    if request.method == 'POST':
        form = FreelancerSearchForm(request.POST)
        if form.is_valid():
            # Get recruiter inputs
            recruiter_zip_code = form.cleaned_data['recruiter_zip_code']
            commute_limit_miles = form.cleaned_data['commute_limit_miles']

            # Redirect to results page with inputs as GET parameters
            return HttpResponseRedirect(reverse('employer_search:search_results') + f'?zip={recruiter_zip_code}&miles={commute_limit_miles}')
    else:
        form = FreelancerSearchForm()

    return render(request, 'employer_search/search_freelancers.html', {'form': form})


def search_results(request):
    """ View to display freelancers that match recruiter zip code and commute limit """
    recruiter_zip_code = request.GET.get('zip')
    commute_limit_miles = int(request.GET.get('miles', 50))  # Default to 50 miles if not provided

    # Assuming you have a function or service to get coordinates from zip code
    recruiter_location = get_coordinates_from_zip(recruiter_zip_code)

    # Retrieve all freelancer profiles
    freelancers = Profile.objects.all()

    # Filter freelancers based on commute distance
    matching_freelancers = []
    for freelancer in freelancers:
        freelancer_location = get_coordinates_from_zip(freelancer.residential_zip_address)
        if freelancer_location:
            # Calculate the distance between recruiter and freelancer
            distance = geodesic(recruiter_location, freelancer_location).miles
            if distance <= commute_limit_miles:
                matching_freelancers.append(freelancer)

    # Pass the matching freelancers to the template for display
    context = {
        'matching_freelancers': matching_freelancers,
        'recruiter_zip_code': recruiter_zip_code,
        'commute_limit_miles': commute_limit_miles,
    }
    return render(request, 'employer_search/search_results.html', context)


# Utility function to get coordinates from a zip code (use an appropriate API or database)
def get_coordinates_from_zip(zip_code):
    """
    Placeholder for getting coordinates (latitude, longitude) from zip code.
    You can implement this using a real service like Google Maps API or GeoPy.
    """
    # Example response for a valid zip code lookup
    zip_code_coordinates = {
        '90210': (34.0901, -118.4065),  # Example: Beverly Hills
        '10001': (40.7128, -74.0060),   # Example: New York City
        # Add more zip codes as needed
    }

    return zip_code_coordinates.get(zip_code)
