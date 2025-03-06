import random
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class EmailSender:
    @staticmethod
    def send_otp_email(user, otp):
        mail_subject = "Activate your account."
        message = render_to_string(
            "activate_account.html",
            {
                "user": user,
                "otp": otp,
            },
        )

        try:
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"
            res = email.send()
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")
