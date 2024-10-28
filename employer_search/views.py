# /Users/2021sam/apps/zyxe/pro/employer_search/views.py


from django.views import View
from django.shortcuts import render, get_object_or_404
from freelancer_profile.models import FreelancerProfile
from employer_job.models import EmployerJob
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Initialize the geolocator instance
geolocator = Nominatim(user_agent="employer_search")  # Replace "your_app_name" with your actual app name

def get_coordinates_from_zip(zip_code):
    """Utility function to get latitude and longitude from a zip code."""
    location = geolocator.geocode(zip_code)
    return (location.latitude, location.longitude) if location else (None, None)

class SearchFreelancersByJobView(View):
    """
    Search for freelancers that match an employer's job posting.
    Filters based on job title, job zip code, and commute limit.
    """

    def get(self, request, job_id):
        # Get the employer job posting
        employer_job = get_object_or_404(EmployerJob, id=job_id)

        # Debugging info to ensure job data is correct
        print(f"Employer Job Title: {employer_job.title}")
        print(f"Employer Job Location: {employer_job.job_zip_code}")
        print(f"Commute Limit: {employer_job.commute_limit_miles}")

        # Get the recruiter location from the employer job's zip code
        recruiter_location = get_coordinates_from_zip(employer_job.job_zip_code)

        # Get all freelancers
        all_freelancers = FreelancerProfile.objects.all()
        print(f'all_freelancers: {all_freelancers}')

        # List to store freelancers who match search criteria
        matching_freelancers = []

        for freelancer in all_freelancers:
            print(f'freelancer.residential_zip_code: {freelancer.residential_zip_code}')
            freelancer_location = get_coordinates_from_zip(freelancer.residential_zip_code)
            print(f'freelancer_location: {freelancer_location}')

            if freelancer_location:
                # Calculate the distance between employer job location and freelancer location
                distance = geodesic(recruiter_location, freelancer_location).miles
                print(f'distance: {distance}')

                # Check if the freelancer is within the commute limit and if job titles match
                if distance <= employer_job.commute_limit_miles and distance <= freelancer.commute_limit_miles:
                    if employer_job.title.lower() in freelancer.desired_job_title.lower():
                        matching_freelancers.append(freelancer)

        # Debugging to confirm the number of matching freelancers
        print(f"Freelancers found: {len(matching_freelancers)}")

        return render(request, 'employer_search/search_freelancers.html', {
            'freelancers': matching_freelancers,
            'employer_job': employer_job,
        })






# from django.shortcuts import render, get_object_or_404
# from freelancer_profile.models import FreelancerProfile
# from employer_job.models import EmployerJob
# from geopy.distance import geodesic
# from geopy.geocoders import Nominatim
#
# # Initialize the geolocator instance
# geolocator = Nominatim(user_agent="employer_search")
#
# def search_freelancers_by_job(request, job_id):
#     """
#     Search for freelancers that match an employer's job posting.
#     Filters based on job title, job zip code, and commute limit.
#     """
#     # Get the employer job posting
#     employer_job = get_object_or_404(EmployerJob, id=job_id)
#
#     # Retrieve employer job location
#     recruiter_location = get_coordinates_from_zip(employer_job.job_zip_code)
#     if recruiter_location == (None, None):
#         # Handle the case where the job's zip code cannot be geolocated
#         return render(request, 'employer_search/error.html', {
#             'error_message': 'Invalid job location. Please check the job zip code.'
#         })
#
#     # Debugging info to ensure job data is correct
#     print(f"Employer Job Title: {employer_job.title}")
#     print(f"Employer Job Location: {employer_job.job_zip_code}")
#     print(f"Commute Limit (Miles): {employer_job.commute_limit_miles}")
#
#     # Get all freelancers
#     all_freelancers = FreelancerProfile.objects.all()
#     print(f'All Freelancers: {len(all_freelancers)}')
#
#     # List to store freelancers who match search criteria
#     matching_freelancers = []
#
#     for freelancer in all_freelancers:
#         freelancer_location = get_coordinates_from_zip(freelancer.residential_zip_code)
#
#         # Check if freelancer's zip code is geocoded successfully
#         if freelancer_location == (None, None):
#             full_name = f"{freelancer.first_name} {freelancer.last_name}"
#             print(f"Skipping freelancer {full_name} due to invalid residential zip code.")
#             continue
#
#         # Calculate the distance between employer job location and freelancer location
#         distance = geodesic(recruiter_location, freelancer_location).miles
#         print(f"Distance to freelancer {freelancer.full_name}: {distance} miles")
#
#         # Check if the freelancer is within both employer and freelancer commute limits
#         if distance <= employer_job.commute_limit_miles and distance <= freelancer.commute_limit_miles:
#             # Check if the job title matches the freelancer's desired job title
#             if employer_job.title.lower() in freelancer.desired_job_title.lower():
#                 matching_freelancers.append(freelancer)
#                 print(f"Freelancer {freelancer.full_name} matches the job criteria.")
#             else:
#                 print(f"Freelancer {freelancer.full_name} does not match job title criteria.")
#         else:
#             print(f"Freelancer {freelancer.full_name} is out of commute range.")
#
#     # Debugging to confirm the number of matching freelancers
#     print(f"Matching Freelancers Found: {len(matching_freelancers)}")
#
#     return render(request, 'employer_search/search_freelancers.html', {
#         'freelancers': matching_freelancers,
#         'employer_job': employer_job,
#     })
#
#


"""
/Users/2021sam/apps/zyxe/pro/employer_search/views.py
Freelancer Search by Employer Job

This search function is designed to find freelancers who match a specific employer job posting.
The search criteria are as follows:

1. **Job Title Matching**:
   The freelancer's `desired_job_title` must match (case-insensitive) the employer's job `title`.

2. **Commute Distance**:
   The freelancer's residential location (based on zip code) must be within:
     - The employer's commute limit (as defined in the employer job posting).
     - The freelancer's own commute limit, ensuring that the freelancer is also willing to travel within that range.

3. **Geolocation Lookup**:
   The latitude and longitude of both the employer's job location and the freelancer's residential location are determined using the `geopy` library.
   The `geodesic` function calculates the distance between these two locations in miles.

4. **Error Handling**:
   If any zip code (either employer's or freelancer's) cannot be geocoded (converted to coordinates), those records are excluded from the matching process.
"""

# from django.shortcuts import render, get_object_or_404
# from freelancer_profile.models import FreelancerProfile
# from employer_job.models import EmployerJob
# from geopy.distance import geodesic
#
#
# def search_freelancers_by_job(request, job_id):
#     """
#     Search for freelancers that match an employer's job posting.
#     Filters based on job title, job zip code, and commute limit.
#     """
#     # Get the employer job posting
#     employer_job = get_object_or_404(EmployerJob, id=job_id)
#
#     # Debugging info to ensure job data is correct
#     print(f"Employer Job Title: {employer_job.title}")
#     print(f"Employer Job Location: {employer_job.job_zip_code}")
#     print(f"Commute Limit: {employer_job.commute_limit_miles}")
#
#     # Get the recruiter location from the employer job's zip code
#     recruiter_location = get_coordinates_from_zip(employer_job.job_zip_code)
#
#     # Get all freelancers
#     all_freelancers = FreelancerProfile.objects.all()
#     print(f'all_freelancers: {all_freelancers}')
#
#     # List to store freelancers who match search criteria
#     matching_freelancers = []
#
#     for freelancer in all_freelancers:
#         print(f'freelancer.residential_zip_code: {freelancer.residential_zip_code}')
#         freelancer_location = get_coordinates_from_zip(freelancer.residential_zip_code)
#         print(f'freelancer_location: {freelancer_location}')
#         if freelancer_location:
#             # Calculate the distance between employer job location and freelancer location
#             distance = geodesic(recruiter_location, freelancer_location).miles
#             print(f'distance: {distance}')
#
#             # Check if the freelancer is within the commute limit and if job titles match
#             if distance <= employer_job.commute_limit_miles:
#                 if distance <= freelancer.commute_limit_miles:
#                     if employer_job.title.lower() in freelancer.desired_job_title.lower():
#                         matching_freelancers.append(freelancer)
#
#     # Debugging to confirm the number of matching freelancers
#     print(f"Freelancers found: {len(matching_freelancers)}")
#
#     return render(request, 'employer_search/search_freelancers.html', {
#         'freelancers': matching_freelancers,
#         'employer_job': employer_job,
#     })
#
#
#
# from geopy.distance import geodesic
# from geopy.geocoders import Nominatim
#
# # Initialize the geolocator instance
# geolocator = Nominatim(user_agent="employer_search")  # Replace "your_app_name" with your actual app name
#
# def get_coordinates_from_zip(zip_code):
#     """Utility function to get latitude and longitude from a zip code."""
#     location = geolocator.geocode(zip_code)
#     return (location.latitude, location.longitude) if location else (None, None)
