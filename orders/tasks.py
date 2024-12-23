import os
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from orders.models import Order, Coupon


@shared_task
def send_order_confirmation_email(order_id, user_email):
    """
        Task to send an order confirmation email to the user.

        Args:
            order_id (int): The ID of the placed order.
            user_email (str): The email address of the user.

        Returns:
            str: Status message indicating success or failure.
    """
    try:
        order = Order.objects.get(pk=order_id)
        send_mail(
            'Order Confirmation',
            f'Your order "{order.course.title}" was placed successfully!',
            os.getenv('EMAIL_HOST_USER'),
            [user_email],
            fail_silently=False,
        )
        return f"Order confirmation email sent to {user_email} for Order ID: {order_id}"
    except Order.DoesNotExist:
        return f"Order with ID {order_id} does not exist."


@shared_task
def send_coupon_expiry_notification(coupon_id):
    """
    Task to notify the creator of a coupon that's nearing its expiration.

    Args:
        coupon_id (int): The ID of the coupon to notify about.

    Returns:
        str: Status message indicating success or failure.
    """
    try:
        coupon = Coupon.objects.get(id=coupon_id)
        if coupon.is_active and not coupon.notified:
            send_mail(
                subject="Your Coupon is About to Expire!",
                message=f"Hi {coupon.creator.username},\n\nYour coupon '{coupon.code}' "
                        f"will expire on {coupon.valid_until.strftime('%Y-%m-%d %H:%M:%S')}. "
                        "Make sure your users take advantage of it before time runs out!",
                from_email=os.getenv('EMAIL_HOST_USER'),
                recipient_list=[coupon.creator.email],
                fail_silently=False,
            )

            coupon.notified = True
            coupon.save()
            return f"Expiry notification sent for Coupon ID: {coupon_id}"

    except Coupon.DoesNotExist:
        return f"Coupon with ID {coupon_id} does not exist."
    except Exception as e:
        return str(e)


@shared_task
def scan_and_notify_expiring_coupons():
    """
    Task to identify and notify about coupons that are expiring soon.

    Coupons that are within 2 days of expiration and still active are included in the notification process.

    Returns:
        str: Status message indicating the number of expiring coupons found and notified.
    """
    expiration_threshold = now() + timedelta(days=2)

    expiring_coupons = Coupon.objects.filter(
        valid_until__lte=expiration_threshold,
        valid_until__gte=now(),
        is_active=True,
        notified=False
    )

    for coupon in expiring_coupons:
        send_coupon_expiry_notification.delay(coupon.id)

    return f"Found and notified for {len(expiring_coupons)} expiring coupons."
