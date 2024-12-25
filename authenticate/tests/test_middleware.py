# pro/authenticate/tests/test_middleware.py
# python manage.py test authenticate.tests.test_middleware
# python manage.py test pro.authenticate.tests.test_middleware



from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from authenticate.middleware import EmailVerificationMiddleware, CheckUserSettingsMiddleware, CustomMiddleware
from authenticate.models import UserSetting


User = get_user_model()

class MiddlewareTestCase(TestCase):
    def setUp(self):
        # Set up the request factory
        self.factory = RequestFactory()
        self.public_category_list_url = reverse('public:category_list')  # This should now resolve correctly
        # self.public_item_detail_url = reverse('public:item_detail', args=[1])  # Add a test item_id
        self.public_item_detail_url = reverse('public:item_detail', kwargs={'item_id': 1})
        self.public_paths = [
            reverse('public:index'),
            reverse('public:category_list'),
            reverse('public:item_detail', kwargs={'item_id': 1}),
        ]
        
        # Create test users
        self.active_user = User.objects.create_user(
            username='activeuser', email='active@example.com', password='test1234', is_active=True
        )
        self.inactive_user = User.objects.create_user(
            username='inactiveuser', email='inactive@example.com', password='test1234', is_active=False
        )
        self.user_no_settings = User.objects.create_user(
            username='nosettings', email='nosettings@example.com', password='test1234', is_active=True
        )

    def test_email_verification_middleware_active_user(self):
        """Test EmailVerificationMiddleware for active users."""
        request = self.factory.get('/')
        request.user = self.active_user

        middleware = EmailVerificationMiddleware(lambda r: "OK")
        response = middleware(request)

        self.assertEqual(response, "OK")  # Active users should pass through

    def test_email_verification_middleware_inactive_user(self):
        """Test EmailVerificationMiddleware for inactive users."""
        request = self.factory.get('/')
        request.user = self.inactive_user

        middleware = EmailVerificationMiddleware(lambda r: "OK")
        response = middleware(request)

        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(response.url, reverse('resend_verification'))

    def test_check_user_settings_middleware_user_with_settings(self):
        """Test CheckUserSettingsMiddleware for user with settings."""
        # Add settings to the user
        from authenticate.models import UserSetting
        UserSetting.objects.create(user=self.active_user, role='freelancer')

        request = self.factory.get('/')
        request.user = self.active_user

        middleware = CheckUserSettingsMiddleware(lambda r: "OK")
        response = middleware(request)

        self.assertEqual(response, "OK")  # User with settings should pass through

    def test_check_user_settings_middleware_user_without_settings(self):
        """Test CheckUserSettingsMiddleware for user without settings."""
        request = self.factory.get('/')
        request.user = self.user_no_settings

        middleware = CheckUserSettingsMiddleware(lambda r: "OK")
        response = middleware(request)

        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(response.url, reverse('initialize_settings'))

    def test_custom_middleware_public_path(self):
        """Test CustomMiddleware for public paths."""
        for path in self.public_paths:
            request = self.factory.get(path)
            request.user = None  # Public paths don't require authentication

            middleware = CustomMiddleware(lambda r: "OK")
            response = middleware(request)

            self.assertEqual(response, "OK")  # Public paths should pass through

    def test_custom_middleware_inactive_user(self):
        """Test CustomMiddleware for inactive authenticated user."""
        request = self.factory.get('/')
        request.user = self.inactive_user

        middleware = CustomMiddleware(lambda r: "OK")
        response = middleware(request)

        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(response.url, reverse('resend_verification'))

    def test_custom_middleware_active_user(self):
        """Test CustomMiddleware for active authenticated user."""
        request = self.factory.get('/')
        request.user = self.active_user

        middleware = CustomMiddleware(lambda r: "OK")
        response = middleware(request)

        self.assertEqual(response, "OK")  # Active users should pass through




from django.urls import reverse

class URLTestCase(TestCase):
    def test_reverse_item_detail(self):
        url = reverse('public:item_detail', kwargs={'item_id': 1})
        self.assertEqual(url, '/public_market/item_detail/1/')
