from uuid import UUID

from apps.stt.models import User
from apps.stt.tasks import send_email_confirmed
from apps.stt.utils import invalidate_user_auth_token
from apps.users.tasks import send_email_change_confirmed
from config.components.celery import CELERY_GENERAL_COUNTDOWN
from config.components.redis import redis_general_connection
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class VerificationService:
    @staticmethod
    def _decode_uid(uidb64: str) -> UUID:
        """Decode the base64-encoded UID and return a UUID object."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return UUID(uid)
        except (ValueError, TypeError):
            raise ValueError('Invalid user ID format')

    @staticmethod
    def _get_user_by_id(user_id: UUID) -> User:
        """Retrieve a user by their UUID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError('User not found')

    @staticmethod
    def _check_token(user: User, token: str) -> None:
        """Check if the token is valid for the given user."""
        if not default_token_generator.check_token(user, token):
            raise ValueError('Token is not valid')

    @staticmethod
    def verify_user(uidb64: str, token: str, new_password: str | None = None) -> str:
        """
        Verify the user based on the UID and token provided. If a new password is provided,
        reset the password. If not, perform standard verification or email change verification.

        :param uidb64: The user's ID encoded in base64.
        :param token: Token for verification.
        :param new_password: New password to set for the user, if applicable.
        :return: A message indicating the result of the verification.
        :raises ValueError: If the UID format is invalid, user is not found, or token is not valid.
        """
        user_id = VerificationService._decode_uid(uidb64)
        user = VerificationService._get_user_by_id(user_id)
        VerificationService._check_token(user, token)

        if new_password:
            return VerificationService._reset_password(user, new_password)

        return VerificationService._process_verification_flow(user, user_id)

    @staticmethod
    def _reset_password(user: User, new_password: str) -> str:
        """Reset the user's password and log out the user."""
        invalidate_user_auth_token(user)
        user.set_password(new_password)
        user.save()
        return 'Password has been reset successfully'

    @staticmethod
    def _process_verification_flow(user: User, user_id: UUID) -> str:
        """Determine the verification flow and process accordingly."""
        new_email = redis_general_connection.get(f'email_change_{user_id}')
        if new_email:
            return VerificationService._process_email_change(user, new_email)
        else:
            return VerificationService._process_standard_verification(user)

    @staticmethod
    def _process_standard_verification(user: User) -> str:
        """
        Process the standard user verification.

        :param user: The user instance to verify.
        :return: A message indicating that standard verification was successful.
        :raises ValueError: If the user is already verified.
        """
        if user.is_verified:
            raise ValueError('User already verified')

        user.is_verified = True
        user.save()

        send_email_confirmed.apply_async(args=(user.email,), countdown=CELERY_GENERAL_COUNTDOWN)

        return 'Standard verification successful'

    @staticmethod
    def _process_email_change(user: User, new_email: str) -> str:
        """
        Process the user's email change verification and log out the user.

        :param user: The user instance to update.
        :param new_email: The new email to set for the user.
        :return: A message indicating that the email change verification was successful.
        """
        invalidate_user_auth_token(user)

        user.email = new_email
        user.username = new_email
        user.save()

        redis_general_connection.delete(f'email_change_{user.id}')
        send_email_change_confirmed.apply_async(args=(new_email,), countdown=CELERY_GENERAL_COUNTDOWN)

        return 'Email change verification successful'
