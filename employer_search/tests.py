from django.test import TestCase
from django.urls import reverse
from freelancer_profile.models import Freelancer  # Make sure the correct model is imported

class SearchFreelancerTestCase(TestCase):

    def test_no_freelancers_found(self):
        # Ensure no freelancers are created
        response = self.client.get(reverse('employer_search:search_freelancers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No matching freelancers found')

    def test_search_freelancers_within_range(self):
        # Create a mock freelancer to test the search functionality
        freelancer = Freelancer.objects.create(username='freelancer1')  # Adjust fields as per your model
        response = self.client.get(reverse('employer_search:search_freelancers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, freelancer.username)  # Check for freelancer in response
