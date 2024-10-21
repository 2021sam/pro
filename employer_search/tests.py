from django.test import TestCase
from django.contrib.auth import get_user_model
from freelancer_profile.models import FreelancerProfile
from geopy.distance import geodesic

User = get_user_model()

class FreelancerProfileSearchTest(TestCase):
    def setUp(self):
        # Create users for testing
        self.user_within_range = User.objects.create_user(
            username='user_within_range', password='password'
        )
        self.freelancer_within_range = FreelancerProfile.objects.create(
            user=self.user_within_range,
            residential_zip_code='94506',
            # Add other necessary fields with appropriate values
        )

        self.user_out_of_range = User.objects.create_user(
            username='user_out_of_range', password='password'
        )
        self.freelancer_out_of_range = FreelancerProfile.objects.create(
            user=self.user_out_of_range,
            residential_zip_code='94507',  # This zip code is out of range
            # Add other necessary fields with appropriate values
        )

        self.user_no_profile = User.objects.create_user(
            username='user_no_profile', password='password'
        )

    def test_search_freelancers_within_range(self):
        # Simulate a search for freelancers within a specific zip code range
        employer_location = (37.8219, -121.9996)  # 94506 coordinates
        freelancer_location = (37.7864, -121.9816)  # 94526 coordinates

        distance = geodesic(employer_location, freelancer_location).miles

        # Check if the distance is within the specified commute limit (e.g., 5 miles)
        self.assertTrue(distance <= 5)  # Adjust as necessary for your test criteria

    def test_search_freelancers_out_of_zip_code_range(self):
        employer_location = (37.8219, -121.9996)  # 94506 coordinates
        freelancer_location = (37.8456, -122.0312)  # 94507 coordinates

        distance = geodesic(employer_location, freelancer_location).miles

        # Check if the distance is greater than the specified commute limit (e.g., 5 miles)
        self.assertTrue(distance > 5)  # Adjust as necessary for your test criteria

    def test_search_freelancers_no_results(self):
        # Simulate a search that returns no results
        employer_location = (37.8219, -121.9996)  # 94506 coordinates
        freelancer_location = (37.0000, -121.0000)  # Out of range coordinates

        distance = geodesic(employer_location, freelancer_location).miles
        self.assertEqual(distance, 0)  # No freelancers should be found
