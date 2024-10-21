from django.test import TestCase
from django.contrib.auth import get_user_model
from freelancer_profile.models import FreelancerProfile
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

User = get_user_model()

class FreelancerProfileSearchTest(TestCase):
    def setUp(self):
        # Create users for testing
        self.user_within_range = User.objects.create_user(
            username='user_within_range', password='password'
        )
        self.freelancer_within_range = FreelancerProfile.objects.create(
            user=self.user_within_range,
            residential_zip_code='94506',  # Danville, CA
        )

        self.user_out_of_range = User.objects.create_user(
            username='user_out_of_range', password='password'
        )
        self.freelancer_out_of_range = FreelancerProfile.objects.create(
            user=self.user_out_of_range,
            residential_zip_code='94507',  # Alamo, CA
        )

        self.user_no_profile = User.objects.create_user(
            username='user_no_profile', password='password'
        )

        # Geolocator for converting zip codes to lat/lon
        self.geolocator = Nominatim(user_agent="geo_test")

    def get_coordinates_from_zip(self, zip_code):
        """Utility function to get latitude and longitude from a zip code."""
        location = self.geolocator.geocode(zip_code)
        return (location.latitude, location.longitude) if location else (None, None)

    def test_search_freelancers_within_range(self):
        employer_zip_code = '94506'
        freelancer_zip_code = self.freelancer_within_range.residential_zip_code

        # Get the coordinates from zip codes
        employer_location = self.get_coordinates_from_zip(employer_zip_code)
        freelancer_location = self.get_coordinates_from_zip(freelancer_zip_code)

        # Ensure coordinates are valid
        self.assertIsNotNone(employer_location[0], "Employer location not found.")
        self.assertIsNotNone(freelancer_location[0], "Freelancer location not found.")

        # Calculate the geodesic distance
        distance = geodesic(employer_location, freelancer_location).miles

        # The distance should be within a 5-mile commute range
        self.assertTrue(distance <= 5, f"Expected distance <= 5 miles, got {distance}")

    def test_search_freelancers_out_of_zip_code_range(self):
        employer_zip_code = '94506'
        freelancer_zip_code = self.freelancer_out_of_range.residential_zip_code

        # Get the coordinates from zip codes
        employer_location = self.get_coordinates_from_zip(employer_zip_code)
        freelancer_location = self.get_coordinates_from_zip(freelancer_zip_code)

        # Ensure coordinates are valid
        self.assertIsNotNone(employer_location[0], "Employer location not found.")
        self.assertIsNotNone(freelancer_location[0], "Freelancer location not found.")

        # Calculate the geodesic distance
        distance = geodesic(employer_location, freelancer_location).miles

        # Adjust the commute limit to check if it's outside a 5-mile range
        self.assertTrue(distance > 5, f"Expected distance > 5 miles, got {distance}")

    def test_search_freelancers_no_results(self):
        employer_zip_code = '94506'
        freelancer_zip_code = '99999'  # A zip code far away

        # Get the coordinates from zip codes
        employer_location = self.get_coordinates_from_zip(employer_zip_code)
        freelancer_location = self.get_coordinates_from_zip(freelancer_zip_code)

        # Ensure coordinates are valid
        self.assertIsNotNone(employer_location[0], "Employer location not found.")
        self.assertIsNotNone(freelancer_location[0], "Freelancer location not found.")

        # Calculate the geodesic distance
        distance = geodesic(employer_location, freelancer_location).miles

        # The distance should be significantly higher than any reasonable commute range
        self.assertTrue(distance > 50, f"Expected no match for distance {distance} miles")
