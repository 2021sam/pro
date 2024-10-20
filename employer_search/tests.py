from django.test import TestCase
from django.urls import reverse
from authenticate.models import CustomUser  # Import your CustomUser model
from freelancer_profile.models import FreelancerProfile

class SearchFreelancerTestCase(TestCase):

    def setUp(self):
        # Create a mock freelancer using CustomUser
        self.user = CustomUser.objects.create_user(username='freelancer1', password='password123')
        self.freelancer_profile = FreelancerProfile.objects.create(user=self.user)

    def test_no_freelancers_found(self):
        # Ensure no freelancers are created other than the one in setUp
        response = self.client.get(reverse('employer_search:search_freelancers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No matching freelancers found')

    def test_search_freelancers_within_range(self):
        # Test the search functionality when a freelancer exists
        response = self.client.get(reverse('employer_search:search_freelancers'))

        # Debug: Print the response content to check why the freelancer is not found
        print(response.content.decode())  # This will output the raw HTML response

        # Check if the user is in the context or response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)  # Check for freelancer username in response
