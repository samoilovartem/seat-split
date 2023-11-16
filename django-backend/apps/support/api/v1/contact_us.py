from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.support.api.serializers import ContactUsSerializer
from apps.support.tasks import send_contact_us_notification
from config.components.celery import CELERY_GENERAL_COUNTDOWN


class ContactView(APIView):
    @swagger_auto_schema(request_body=ContactUsSerializer)
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            inquiry = serializer.save()
            send_contact_us_notification.apply_async(
                args=(
                    inquiry.email,
                    inquiry.subject,
                    inquiry.message,
                    inquiry.first_name,
                    inquiry.last_name,
                ),
                countdown=CELERY_GENERAL_COUNTDOWN,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
