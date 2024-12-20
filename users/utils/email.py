from django.core.mail import send_mail


def send_verification_email(email, code):
    """
    Send the verification code to the user's email.
    """
    subject = "Your Verification Code"
    message = f"Your verification code is {code}. It will expire in 10 minutes."
    sender_email = "meako.sivsivadze@gmail.com"
    recipient_email = [email]

    send_mail(subject, message, sender_email, recipient_email)


def send_success_email(email):
    subject = "Your Email is Verified!"
    message = "Thank you for verifying your email. You can now access your account."
    sender_email = "meako.sivsivadze@gmail.com"
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)


def send_password_reset_email(email, token):
    """
    Sends a password reset email to the user.
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
    Sends an email to notify the user that their password was reset successfully.
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
