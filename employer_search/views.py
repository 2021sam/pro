from django.shortcuts import render, get_object_or_404
from freelancer_profile.models import FreelancerProfile
from employer_job.models import EmployerJob
from geopy.distance import geodesic


def search_freelancers_by_job(request, job_id):
    """
    Search for freelancers that match an employer's job posting.
    Filters based on job title, job zip code, and commute limit.
    """
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

    # List to store freelancers who match search criteria
    matching_freelancers = []

    for freelancer in all_freelancers:
        freelancer_location = get_coordinates_from_zip(freelancer.residential_zip_code)

        if freelancer_location:
            # Calculate the distance between employer job location and freelancer location
            distance = geodesic(recruiter_location, freelancer_location).miles

            # Check if the freelancer is within the commute limit and if job titles match
            if distance <= employer_job.commute_limit_miles and employer_job.title.lower() in freelancer.desired_job_title.lower():
                matching_freelancers.append(freelancer)

    # Debugging to confirm the number of matching freelancers
    print(f"Freelancers found: {len(matching_freelancers)}")

    return render(request, 'employer_search/search_freelancers.html', {
        'freelancers': matching_freelancers,
        'employer_job': employer_job,
    })


def get_coordinates_from_zip(zip_code):
    """
    Placeholder for getting coordinates (latitude, longitude) from zip code.
    You can implement this using a real service like Google Maps API or GeoPy.
    """
    zip_code_coordinates = {
        '90210': (34.0901, -118.4065),  # Example: Beverly Hills
        '10001': (40.7128, -74.0060),  # Example: New York City
        # Add more zip codes as needed
    }
    return zip_code_coordinates.get(zip_code)
