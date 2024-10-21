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


# /Users/2021sam/apps/zyxe/pro/employer_search/tests.py

# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from freelancer_profile.models import FreelancerProfile  # Replace with your actual model
# from freelancer_profile.utils import your_commute_filter_function  # Replace with your actual function
#
#
# class CommuteFilterTestCase(TestCase):
#     def setUp(self):
#         # Create the first user with a unique email
#         user1 = get_user_model().objects.create_user(
#             username='freelancer1',
#             email='freelancer1@example.com',
#             password='password1'
#         )
#
#         # Create the second user with a different unique email
#         user2 = get_user_model().objects.create_user(
#             username='freelancer2',
#             email='freelancer2@example.com',
#             password='password2'
#         )
#
#         # Create instances of the relevant models needed for testing
#         # For example, if you're testing against a model called Job
#         self.job1 = YourModel.objects.create(
#             user=user1,
#             location='Location 1',
#             commute_distance=10  # Example field
#         )
#
#         self.job2 = YourModel.objects.create(
#             user=user2,
#             location='Location 2',
#             commute_distance=25  # Example field
#         )
#
#     def test_commute_filter_within_range(self):
#         # Implement your test logic for checking within range
#         self.assertTrue(your_commute_filter_function(self.job1, user1))
#
#     def test_commute_filter_out_of_range(self):
#         # Implement your test logic for checking out of range
#         self.assertFalse(your_commute_filter_function(self.job2, user1))



from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from employer_job.models import EmployerJob

from freelancer_profile.models import FreelancerProfile

class CommuteFilterTestCase(TestCase):
    def setUp(self):
        # Create users with unique emails to avoid IntegrityError
        user1 = get_user_model().objects.create_user(
            username='freelancer1',
            email='freelancer1@example.com',
            password='password1'
        )
        user2 = get_user_model().objects.create_user(
            username='freelancer2',
            email='freelancer2@example.com',
            password='password2'
        )

        # Create freelancer profiles for the users
        FreelancerProfile.objects.create(user=user1, zip_code='10001', commute_limit=10)
        FreelancerProfile.objects.create(user=user2, zip_code='10002', commute_limit=5)

        # Create job listings
        Job.objects.create(title='Job 1', zip_code='10001', commute_limit=15)
        Job.objects.create(title='Job 2', zip_code='10003', commute_limit=5)

    def test_commute_filter_within_range(self):
        # Simulate accessing the job listing page
        self.client.login(username='freelancer1', password='password1')
        response = self.client.get(reverse('job_listing'))

        # Check that the correct freelancers are listed
        self.assertContains(response, 'freelancer1')
        self.assertNotContains(response, 'freelancer2')

    def test_commute_filter_out_of_range(self):
        # Simulate accessing the job listing page
        self.client.login(username='freelancer2', password='password2')
        response = self.client.get(reverse('job_listing'))

        # Check that the correct freelancers are listed
        self.assertContains(response, 'freelancer2')
        self.assertNotContains(response, 'freelancer1')

