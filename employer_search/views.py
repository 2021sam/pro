# /Users/2021sam/apps/zyxe/pro/employer_search/views.py
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


from django.views import View
from django.shortcuts import render, get_object_or_404
from freelancer_profile.models import FreelancerProfile
from employer_job.models import EmployerJob
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Initialize the geolocator instance
geolocator = Nominatim(user_agent="employer_search")


def get_coordinates_from_zip_and_state(zip_code, state, country='USA'):
    """Utility function to get latitude and longitude from a zip code and state."""
    geolocator = Nominatim(user_agent="geo_test")

    # Print the zip code and state being used
    print(f"Geolocating for ZIP: {zip_code}, State: {state}")

    # Attempt to get the coordinates
    location = geolocator.geocode(f"{zip_code}, {state}, {country}")

    # Print the location details returned
    if location:
        print(f"Coordinates found: {location.latitude}, {location.longitude}")
        return (location.latitude, location.longitude)
    else:
        print(f"No coordinates found for {zip_code}, {state}")
        return (None, None)


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
        print(f"Employer Job Location: {employer_job.job_zip_code}, {employer_job.job_state}")
        print(f"Employer Commute Limit: {employer_job.commute_limit_miles}")

        # Get the employer (recruiter) location from the employer job's zip code and state
        recruiter_location = get_coordinates_from_zip_and_state(employer_job.job_zip_code, employer_job.job_state)

        if recruiter_location == (None, None):
            return render(request, 'employer_search/error.html', {
                'error_message': 'Invalid job location. Please check the job zip code and state.'
            })

        # Get all freelancers
        all_freelancers = FreelancerProfile.objects.all()
        print(f"Total Freelancers: {len(all_freelancers)}")

        # List to store freelancers who match search criteria
        matching_freelancers = []

        for freelancer in all_freelancers:
            print(f"Freelancer ZIP: {freelancer.residential_zip_code}")
            freelancer_location = get_coordinates_from_zip_and_state(freelancer.residential_zip_code,
                                                                     freelancer.residential_state)

            if freelancer_location:
                # Calculate the distance between employer job location and freelancer location
                distance = geodesic(recruiter_location, freelancer_location).miles
                print(f"Distance between employer and freelancer: {distance} miles")

                # Check if the freelancer is within both the employer's and freelancer's commute limits
                if distance <= employer_job.commute_limit_miles and distance <= freelancer.commute_limit_miles:
                    if employer_job.title.lower() in freelancer.desired_job_title.lower():
                        # Use first_name and last_name if full_name doesn't exist
                        freelancer_full_name = f"{freelancer.first_name} {freelancer.last_name}"
                        matching_freelancers.append(freelancer)
                        print(f"Freelancer {freelancer_full_name} matches the job criteria.")
                    else:
                        print(
                            f"Freelancer {freelancer.first_name} {freelancer.last_name} does not match job title criteria.")
                else:
                    print(f"Freelancer {freelancer.first_name} {freelancer.last_name} is out of commute range.")

        # Debugging to confirm the number of matching freelancers
        print(f"Total Matching Freelancers: {len(matching_freelancers)}")

        return render(request, 'employer_search/search_freelancers.html', {
            'freelancers': matching_freelancers,
            'employer_job': employer_job,
        })



    def post(self, request, job_id):
        # Get the freelancer ID and the decision (Interested or Reject)
        freelancer_id = request.POST.get('freelancer_id')
        decision = request.POST.get('decision')

        # Logic to handle the decision (e.g., save to the database)
        # Here you would implement your EmployerDecision model logic
        # For example, you might do something like this:
        # EmployerDecision.objects.create(employer_job_id=job_id, freelancer_id=freelancer_id, decision=decision)

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success', 'message': f'Decision recorded: {decision}'})






# /Users/2021sam/apps/zyxe/pro/employer_search/views.py

from django.views import View
from django.http import JsonResponse
from .models import EmployerDecision
from freelancer_profile.models import FreelancerProfile

class EmployerDecisionView(View):
    def post(self, request, freelancer_id, job_id):
        action = request.POST.get('action')
        freelancer = FreelancerProfile.objects.get(id=freelancer_id)

        # Create or update the decision record
        decision, created = EmployerDecision.objects.get_or_create(freelancer=freelancer, job_id=job_id)

        if action == 'interested':
            decision.interested = True
            decision.rejected = False
        elif action == 'rejected':
            decision.rejected = True
            decision.interested = False

        decision.save()
        return JsonResponse({'success': True})


# /Users/2021sam/apps/zyxe/pro/employer_search/views.py

from django.views import View
from django.http import JsonResponse
from freelancer_profile.models import FreelancerProfile
from .models import EmployerDecision






# /Users/2021sam/apps/zyxe/pro/employer_search/views.py

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')  # CSRF exemption if necessary
class UpdateEmployerDecisionView(View):
    def post(self, request, job_id, freelancer_id):
        decision = request.POST.get('decision')

        # Logic to handle the decision here
        # For example, save the decision to the database

        # Assuming the decision was processed successfully
        return JsonResponse({
            'status': 'success',
            'message': f'Decision recorded: {decision}'
        })
