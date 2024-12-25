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
        self.factory = RequestFactory()
        self.public_category_list_url = reverse('public:category_list')
        self.public_item_detail_url = reverse('public:item_detail', kwargs={'item_id': 1})
        self.public_paths = [
            reverse('public:index'),
            reverse('public:category_list'),
            reverse('public:item_detail', kwargs={'item_id': 1}),
        ]

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
        request = self.factory.get('/')
        request.user = self.active_user
        middleware = EmailVerificationMiddleware(lambda r: "OK")
        response = middleware(request)
        self.assertEqual(response, "OK")

    def test_email_verification_middleware_inactive_user(self):
        request = self.factory.get('/')
        request.user = self.inactive_user
        middleware = EmailVerificationMiddleware(lambda r: "OK")
        response = middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('resend_verification'))

    def test_check_user_settings_middleware_user_with_settings(self):
        UserSetting.objects.create(user=self.active_user, role='freelancer')
        request = self.factory.get('/')
        request.user = self.active_user
        middleware = CheckUserSettingsMiddleware(lambda r: "OK")
        response = middleware(request)
        self.assertEqual(response, "OK")

    def test_check_user_settings_middleware_user_without_settings(self):
        request = self.factory.get('/')
        request.user = self.user_no_settings
        middleware = CheckUserSettingsMiddleware(lambda r: "OK")
        response = middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('initialize_settings'))

    def test_custom_middleware_public_path(self):
        for path in self.public_paths:
            request = self.factory.get(path)
            request.user = None
            middleware = CustomMiddleware(lambda r: "OK")
            response = middleware(request)
            self.assertEqual(response, "OK")

    def test_custom_middleware_inactive_user(self):
        request = self.factory.get('/')
        request.user = self.inactive_user
        middleware = CustomMiddleware(lambda r: "OK")
        response = middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('resend_verification'))

    def test_custom_middleware_active_user(self):
        request = self.factory.get('/')
        request.user = self.active_user
        middleware = CustomMiddleware(lambda r: "OK")
        response = middleware(request)
        self.assertEqual(response, "OK")

class URLTestCase(TestCase):
    def test_reverse_item_detail(self):
        url = reverse('public:item_detail', kwargs={'item_id': 1})
        self.assertEqual(url, '/public_market/item_detail/1/')
