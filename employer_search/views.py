from django.shortcuts import render
from .forms import FreelancerSearchForm  # Assuming a form for entering job zip code and commute limit
from freelancer_profile.models import FreelancerProfile
from geopy.distance import geodesic  # For calculating distances between zip codes  pip install geopy
from django.http import HttpResponseRedirect
from django.urls import reverse

# from django.shortcuts import render
from django.db.models import Q
# from .models import FreelancerProfile

def search_freelancers(request):
    # Get the search parameters from the request
    job_title = request.GET.get('job_title', '')
    work_authorization = request.GET.get('work_authorization', '')
    location_preference = request.GET.get('location_preference', '')
    commute_limit_miles = request.GET.get('commute_limit_miles', '')
    
    # Print out the values to debug
    print(f"Job title search: {job_title}")
    print(f"Work authorization search: {work_authorization}")
    print(f"Location preference search: {location_preference}")
    print(f"Commute limit miles search: {commute_limit_miles}")
    
    # Create a Q object for searching based on parameters
    query = Q()
    
    if job_title:
        query &= Q(desired_job_title__icontains=job_title)
        print(f"Job title filter applied: {query}")
    
    if work_authorization:
        query &= Q(work_authorization=work_authorization)
        print(f"Work authorization filter applied: {query}")
    
    if location_preference:
        query &= Q(location_preference=location_preference)
        print(f"Location preference filter applied: {query}")
    
    if commute_limit_miles:
        try:
            commute_limit_miles = int(commute_limit_miles)
            query &= Q(commute_limit_miles__lte=commute_limit_miles)
            print(f"Commute limit filter applied: {query}")
        except ValueError:
            print(f"Invalid commute limit miles: {commute_limit_miles}")
    
    # Print the final query to check if it's correct
    print(f"Final Query: {query}")
    
    # Filter the FreelancerProfile model based on the query
    freelancers = FreelancerProfile.objects.filter(query)
    
    # Print the count of matching freelancers to see if any were found
    print(f"Freelancers found: {freelancers.count()}")

    # Render the search results page
    return render(request, 'employer_search/search_freelancers.html', {'freelancers': freelancers})


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
