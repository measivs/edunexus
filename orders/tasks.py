from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from orders.models import Order, Coupon


@shared_task
def send_order_confirmation_email(order_id, user_email):
    try:
        order = Order.objects.get(pk=order_id)
        send_mail(
            'Order Confirmation',
            f'Your order "{order.course.title}" was placed successfully!',
            'meako.sivsivadze@gmail.com',
            [user_email],
            fail_silently=False,
        )
        return f"Order confirmation email sent to {user_email} for Order ID: {order_id}"
    except Order.DoesNotExist:
        return f"Order with ID {order_id} does not exist."


@shared_task
def send_coupon_expiry_notification(coupon_id):
    """
    Task to send an email notification about a coupon that's about to expire.
    """
    try:
        coupon = Coupon.objects.get(id=coupon_id)
        if coupon.is_active and not coupon.notified:
            send_mail(
                subject="Your Coupon is About to Expire!",
                message=f"Hi {coupon.creator.username},\n\nYour coupon '{coupon.code}' "
                        f"will expire on {coupon.valid_until.strftime('%Y-%m-%d %H:%M:%S')}. "
                        "Make sure your users take advantage of it before time runs out!",
                from_email='meako.sivsivadze@gmail.com',
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
    Task to find and send notifications for coupons nearing their expiration date.
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

