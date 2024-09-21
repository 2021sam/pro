import logging
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

logger = logging.getLogger(__name__)

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug(f"Trying to authenticate user with email: {username}")
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(email=username))
        except UserModel.DoesNotExist:
            logger.debug(f"User with email {username} not found")
            return None

        if user.check_password(password):
            logger.debug(f"User {username} successfully authenticated")
            return user
        else:
            logger.debug(f"Password mismatch for user {username}")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False
        """
        return getattr(user, 'is_active', False)