from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from freelancer_profile.models import FreelancerProfile

from django.contrib.auth import get_user_model
from freelancer_profile.models import FreelancerProfile
from django.urls import reverse



#   Success
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

    # def test_search_finds_matching_freelancer(self):
    #     # Create a test freelancer in the database
    #     FreelancerProfile.objects.create(
    #         first_name='John',
    #         last_name='Doe',
    #         work_zip_address='90210',
    #         commute_limit_miles=50
    #     )
    #
    #     # Simulate a search that matches the freelancer's criteria
    #     response = self.client.get(reverse('employer_search:search_freelancers'), {
    #         'zip_code': '90210',
    #         'commute_limit': '50'
    #     })
    #
    #     # Check if the freelancer is found in the search results
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'John Doe')  # Check if freelancer is in the response


# from django.contrib.auth import get_user_model
# from freelancer_profile.models import FreelancerProfile


    # def test_search_finds_matching_freelancer(self):
    #     # Create a test user
    #     User = get_user_model()
    #     user = User.objects.create_user(
    #         username='johndoe',
    #         password='password123',
    #         email='johndoe@example.com'
    #     )
    #
    #     # Create a test freelancer profile and link it to the user
    #     FreelancerProfile.objects.create(
    #         user=user,
    #         first_name='John',
    #         last_name='Doe',
    #         work_zip_address='90210',
    #         commute_limit_miles=50
    #     )
    #
    #     # Simulate a search that matches the freelancer's criteria
    #     response = self.client.get(reverse('employer_search:search_freelancers'), {
    #         'zip_code': '90210',
    #         'commute_limit': '50'
    #     })
    #
    #     # Check if the freelancer is found in the search results
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'John Doe')  # Check if freelancer is in the response


    #   success
    def test_search_finds_matching_freelancer(self):
        # Create a test user (CustomUser)
        User = get_user_model()
        user = User.objects.create_user(
            username='johndoe',
            password='password123',
            email='johndoe@example.com'
        )

        # Create a FreelancerProfile linked to the test user
        FreelancerProfile.objects.create(
            user=user,  # Link to CustomUser instance
            first_name='John',
            last_name='Doe',
            work_zip_address='90210',
            commute_limit_miles=50
        )

        # Simulate a search for freelancers
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '90210',
            'commute_limit': '50'
        })

        # Ensure the freelancer appears in the search results
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')  # Verifies the freelancer is in the result







# employer_search/tests.py

from django.test import TestCase
from django.urls import reverse
from freelancer_profile.models import FreelancerProfile
from django.contrib.auth import get_user_model

class CommuteFilterTestCase(TestCase):

    def setUp(self):
        # Create a user and freelancer profiles with different zip codes
        user1 = get_user_model().objects.create(username='freelancer1', password='password1')
        user2 = get_user_model().objects.create(username='freelancer2', password='password2')
        user3 = get_user_model().objects.create(username='freelancer3', password='password3')

        # Freelancer within range
        self.freelancer1 = FreelancerProfile.objects.create(
            user=user1,
            first_name='John',
            last_name='Doe',
            work_zip_address='90210',  # Beverly Hills
        )

        # Freelancer slightly out of range
        self.freelancer2 = FreelancerProfile.objects.create(
            user=user2,
            first_name='Jane',
            last_name='Doe',
            work_zip_address='90001',  # Los Angeles
        )

        # Freelancer far out of range
        self.freelancer3 = FreelancerProfile.objects.create(
            user=user3,
            first_name='Sam',
            last_name='Smith',
            work_zip_address='10001',  # New York
        )

    def test_commute_filter_within_range(self):
        # Test a commute limit that only includes the freelancer within range
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '90210',  # Job zip code (Beverly Hills)
            'commute_limit': 10  # 10 miles commute limit
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')  # Freelancer within range should be found
        self.assertNotContains(response, 'Jane Doe')  # Freelancer out of range shouldn't be found
        self.assertNotContains(response, 'Sam Smith')  # Freelancer far out of range shouldn't be found

    def test_commute_filter_out_of_range(self):
        # Test a commute limit that excludes both freelancers
        response = self.client.get(reverse('employer_search:search_freelancers'), {
            'zip_code': '90210',
            'commute_limit': 5  # 5 miles commute limit, tighter range
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Doe')
        self.assertNotContains(response, 'Sam Smith')
