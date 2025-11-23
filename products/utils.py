from django.core.mail import send_mail
from django.conf import settings

def send_order_email(to_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False
