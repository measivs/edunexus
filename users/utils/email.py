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
