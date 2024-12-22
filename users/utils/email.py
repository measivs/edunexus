from django.core.mail import send_mail


def send_verification_email(email, code):
    """
    Send a verification email containing a 6-digit code.

    Args:
        email (str): The recipient's email address.
        code (str): The 6-digit verification code.
    """
    subject = "Your Verification Code"
    message = f"Your verification code is {code}. It will expire in 10 minutes."
    sender_email = "meako.sivsivadze@gmail.com"
    recipient_email = [email]

    send_mail(subject, message, sender_email, recipient_email)


def send_success_email(email):
    """
        Send an email to notify the user that their email verification was successful.

        Args:
            email (str): The recipient's email address.
    """
    subject = "Your Email is Verified!"
    message = "Thank you for verifying your email. You can now access your account."
    sender_email = "meako.sivsivadze@gmail.com"
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)


def send_password_reset_email(email, token):
    """
    Send an email containing a password reset token to the user.

    Args:
        email (str): The recipient's email address.
        token (str): The password reset token.
    """
    subject = 'Password Reset Request'
    message = (
        f"Hi,\n\n"
        f"We received a request to reset your password. Use the following token to reset your password:\n\n"
        f"{token}\n\n"
        f"If you didn’t request a password reset, please ignore this email.\n\n"
        f"Thanks,\nEduNexus"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email="meako.sivsivadze@gmail.com",
        recipient_list=[email],
    )


def send_password_reset_success_email(email):
    """
    Send an email notifying the user that their password has been successfully reset.

    Args:
        email (str): The recipient's email address.
    """
    subject = "Your Password Has Been Successfully Reset"
    message = (
        "Hello,\n\n"
        "Your password has been successfully reset. "
        "If you did not request this change, please contact support immediately.\n\n"
        "Thank you,\nEduNexus"
    )
    sender_email = "meako.sivsivadze@gmail.com"
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)
