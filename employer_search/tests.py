from django.test import TestCase
from django.urls import reverse
from authenticate.models import CustomUser
from freelancer_profile.models import FreelancerProfile

class SearchFreelancerTestCase(TestCase):
    def setUp(self):
        # Create an employer and a freelancer user
        self.employer_user = CustomUser.objects.create_user(username='employer', password='employerpassword')
        self.freelancer_user = CustomUser.objects.create_user(username='freelancer', password='freelancerpassword')

        # Create a FreelancerProfile for the freelancer
        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.freelancer_user,
            commute_limit_miles=10
        )

    def test_no_freelancers_found(self):
        # Simulate a job posting with a commute limit that doesn't match any freelancer
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '12345',
            'commute_limit': 5
        })
        
        print(f"Status code (no freelancers found): {response.status_code}")
        print(f"Response content (no freelancers found): {response.content.decode()}")  # Print full response content
        
        # Check if the response contains 'No matching freelancers found'
        self.assertContains(response, 'No matching freelancers found')

    def test_search_freelancers_within_range(self):
        # Simulate a job posting with a commute limit that matches the freelancer
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '12345',
            'commute_limit': 10
        })
        
        print(f"Status code (freelancer found): {response.status_code}")
        print(f"Response content (freelancer found): {response.content.decode()}")  # Print full response content
        
        # Check if the response contains the freelancer's username
        self.assertContains(response, 'freelancer')
