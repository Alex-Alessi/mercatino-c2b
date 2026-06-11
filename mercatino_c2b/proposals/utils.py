from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def send_notification_email(subject, message, recipients):
    if not recipients:
        return
    
    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=recipients,
        fail_silently=False,
    )

def get_staff_emails():
    return list(
        User.objects.filter(
            is_staff=True,
            is_active=True,
        )
        .exclude(email="")
        .values_list("email", flat=True)
    )