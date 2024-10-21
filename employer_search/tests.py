# /Users/2021sam/apps/zyxe/pro/employer_search/tests.py
from django.test import TestCase
from django.urls import reverse
from freelancer_profile.models import FreelancerProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class FreelancerProfileSearchTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create freelancer profiles for testing
        self.freelancer_in_range = FreelancerProfile.objects.create(
            user=self.user,
            residential_zip_code='12345',  # This zip code is within range
            # Add other required fields as necessary
        )

        self.freelancer_out_of_range = FreelancerProfile.objects.create(
            user=self.user,
            residential_zip_code='99999',  # This zip code is out of the given range
            # Add other required fields as necessary
        )

    def test_search_freelancers_within_range(self):
        # Test searching freelancers within the specified zip code range
        response = self.client.get(reverse('employer_search:search_freelancers'), {'zip_code': '12345', 'range': 10})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            self.freelancer_in_range.user.username)  # Check if the freelancer is listed in the results
        self.assertNotContains(response,
                               self.freelancer_out_of_range.user.username)  # Ensure out-of-range freelancer is not listed

    def test_search_freelancers_no_results(self):
        # Test searching freelancers when no results should be returned
        response = self.client.get(reverse('employer_search:search_freelancers'), {'zip_code': '99999', 'range': 10})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No freelancers found.")  # Adjust this message based on your implementation

    def test_search_freelancers_out_of_zip_code_range(self):
        # Test searching freelancers outside of the specified zip code range
        response = self.client.get(reverse('employer_search:search_freelancers'), {'zip_code': '12345', 'range': 10})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
                               self.freelancer_out_of_range.user.username)  # Ensure out-of-range freelancer is not listed

