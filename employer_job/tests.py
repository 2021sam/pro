from django.test import TestCase
from django.urls import reverse
from employer_job.models import EmployerJob
from freelancer_profile.models import FreelancerProfile
from django.contrib.auth.models import User

class SearchFreelancerTestCase(TestCase):
    
    def setUp(self):
        # Create users
        self.employer_user = User.objects.create_user(username='employer', password='employerpassword')
        self.freelancer_user_near = User.objects.create_user(username='freelancer_near', password='freelancerpassword')
        self.freelancer_user_far = User.objects.create_user(username='freelancer_far', password='freelancerpassword')

        # Create job posting by employer
        self.job = EmployerJob.objects.create(
            user=self.employer_user,
            title='Test Job',
            description='This is a test job',
            job_zip_code='94506',  # Job located at zip 94506
            commute_limit_miles=50  # 50 miles limit
        )

        # Create freelancer profiles
        self.freelancer_near = FreelancerProfile.objects.create(
            user=self.freelancer_user_near,
            work_zip_address='94507',  # Freelancer close to job (in range)
            commute_limit_miles=50  # Freelancer willing to commute up to 50 miles
        )

        self.freelancer_far = FreelancerProfile.objects.create(
            user=self.freelancer_user_far,
            work_zip_address='90210',  # Freelancer far from job (out of range)
            commute_limit_miles=50  # Freelancer willing to commute up to 50 miles
        )

    def test_search_freelancers_within_range(self):
        # Perform search using the job details
        response = self.client.get(reverse('employer_search:search_freelancers'), {'job_id': self.job.id})

        # Ensure freelancer_near is found
        self.assertContains(response, self.freelancer_near.user.username)
        
        # Ensure freelancer_far is not found
        self.assertNotContains(response, self.freelancer_far.user.username)

    def test_no_freelancers_found(self):
        # Change job's commute limit to be too small
        self.job.commute_limit_miles = 5
        self.job.save()

        # Perform search using the job details
        response = self.client.get(reverse('employer_search:search_freelancers'), {'job_id': self.job.id})

        # Ensure no freelancers are found
        self.assertNotContains(response, self.freelancer_near.user.username)
        self.assertNotContains(response, self.freelancer_far.user.username)

