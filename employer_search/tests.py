from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from freelancer_profile.models import FreelancerProfile

class SearchFreelancerTestCase(TestCase):
    @patch('employer_search.views.get_coordinates_from_zip')
    def test_search_freelancers(self, mock_get_coordinates):
        # Mock the coordinates for the given zip code
        mock_get_coordinates.side_effect = lambda zip_code: (34.0901, -118.4065) if zip_code == '90210' else None

        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '90210',
            'commute_limit': '50'
        })

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employer_search/search_freelancers.html')

        # Ensure the freelancers list is empty as we are not checking the DB
        self.assertContains(response, "No freelancers found within the specified commute limit.")

    def test_search_freelancers_page_loads(self):
        response = self.client.get(reverse('employer_search:search_freelancers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Search Freelancers</h1>')
        self.assertContains(response, 'Enter Job Zip Code')
        self.assertContains(response, 'Commute Limit (miles)')
        self.assertContains(response, '<button type="submit">Search</button>')

    def test_search_form_submission(self):
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '90210',  # Example ZIP code
            'commute_limit': '50'  # Example commute limit
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No freelancers found within the specified commute limit.')


    from freelancer_profile.models import FreelancerProfile

    def test_search_finds_matching_freelancer(self):
        # Create a test freelancer in the database
        FreelancerProfile.objects.create(
            first_name='John',
            last_name='Doe',
            work_zip_address='90210',
            commute_limit_miles=50
        )

        # Simulate a search that matches the freelancer's criteria
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '90210',
            'commute_limit': '50'
        })

        # Check if the freelancer is found in the search results
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')  # Check if freelancer is in the response
