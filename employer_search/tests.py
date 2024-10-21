# employer_search/tests.py
# This only tests for matching zip codes

from django.test import TestCase
from django.contrib.auth import get_user_model
from freelancer_profile.models import FreelancerProfile

User = get_user_model()


class FreelancerProfileSearchTest(TestCase):
    def setUp(self):
        # Create users for testing
        self.user_within_range = User.objects.create_user(
            username='user_within_range', password='password'
        )
        self.freelancer_within_range = FreelancerProfile.objects.create(
            user=self.user_within_range,
            residential_zip_code='12345',
            work_zip_code='12345',
            # Add other necessary fields with appropriate values
        )

        self.user_out_of_range = User.objects.create_user(
            username='user_out_of_range', password='password'
        )
        self.freelancer_out_of_range = FreelancerProfile.objects.create(
            user=self.user_out_of_range,
            residential_zip_code='99999',
            work_zip_code='99999',
            # Add other necessary fields with appropriate values
        )

        self.user_no_profile = User.objects.create_user(
            username='user_no_profile', password='password'
        )

    def test_search_freelancers_within_range(self):
        # Simulate a search for freelancers within a specific zip code range
        results = FreelancerProfile.objects.filter(
            residential_zip_code='12345'  # Simulating a search criteria
        )
        self.assertIn(self.freelancer_within_range, results)
        self.assertNotIn(self.freelancer_out_of_range, results)

    def test_search_freelancers_out_of_zip_code_range(self):
        # Simulate a search for freelancers who are out of the specified range
        results = FreelancerProfile.objects.filter(
            residential_zip_code='99999'  # Simulating a search criteria
        )
        self.assertIn(self.freelancer_out_of_range, results)
        self.assertNotIn(self.freelancer_within_range, results)

    def test_search_freelancers_no_results(self):
        # Simulate a search that returns no results
        results = FreelancerProfile.objects.filter(
            residential_zip_code='00000'  # Simulating a search criteria with no match
        )
        self.assertEqual(results.count(), 0)

