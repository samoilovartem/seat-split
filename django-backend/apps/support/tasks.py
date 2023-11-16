from celery import shared_task
from loguru import logger

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.components.smtp_and_email import EMAIL_CONTENT_TYPE, SMTP2GO_SUPPORT_EMAIL


@shared_task
def send_contact_us_notification(user_email: str, subject: str, message: str):
    """Sends notification to support staff when a contact form is submitted."""
    support_email_body = render_to_string(
        'emails/contact_notification.html',
        {
            'user_email': user_email,
            'message': message,
            'subject': subject,
        },
    )
    email = EmailMessage(
        subject=subject,
        body=support_email_body,
        to=[SMTP2GO_SUPPORT_EMAIL],
        from_email=user_email,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
        logger.info('Contact notification has been successfully sent to support staff.')
    except Exception as e:
        logger.exception('Error sending contact notification: {}', e)
