from uuid import UUID

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from apps.stt.models import User
from apps.stt.tasks import send_email_confirmed
from apps.users.tasks import send_email_change_confirmed
from config.components.celery import CELERY_GENERAL_COUNTDOWN
from config.components.redis import redis_general_connection


class VerificationService:
    @staticmethod
    def verify_user(uidb64, token, new_password=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user_id = UUID(uid)
        except (ValueError, TypeError):
            raise ValueError('Invalid user ID format')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError('User not found')

        if not default_token_generator.check_token(user, token):
            raise ValueError('Token is not valid')

        if new_password:
            user.set_password(new_password)
            user.save()
            return 'Password has been reset successfully'

        new_email = redis_general_connection.get(f'email_change_{uid}')
        is_email_change_verification = bool(new_email)

        if is_email_change_verification:
            return VerificationService._process_email_change(user, new_email, uid)
        else:
            return VerificationService._process_standard_verification(user)

    @staticmethod
    def _process_standard_verification(user):
        if user.is_verified:
            raise ValueError('User already verified')

        user.is_verified = True
        user.save()

        send_email_confirmed.apply_async(
            args=(user.email,), countdown=CELERY_GENERAL_COUNTDOWN
        )
        return 'Standard verification successful'

    @staticmethod
    def _process_email_change(user, new_email, uid):
        user.email = new_email
        user.username = new_email
        user.save()
        redis_general_connection.delete(f'email_change_{uid}')
        send_email_change_confirmed.apply_async(
            args=(new_email,), countdown=CELERY_GENERAL_COUNTDOWN
        )
        return 'Email change verification successful'
