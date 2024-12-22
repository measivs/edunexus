from django.shortcuts import get_object_or_404
from orders.services.order_calculation import calculate_final_price
from users.models import AccountBalance
from courses.models import Course
from orders.models import Order, Coupon


class OrderService:
    """
        A service for handling course orders.

        Initialization Args:
            - `user`: The user placing the order.
            - `course_title`: The title of the course to be ordered.
            - `coupon_code` (optional): Discount coupon code.

        Features:
            - Validates course eligibility.
            - Validates optional coupon eligibility.
            - Calculates the final price including discounts and taxes.
            - Places an order and deducts the user's balance.

        Methods:
            - `validate_coupon`: Ensures the coupon is valid, active, and meets minimum thresholds.
            - `calculate_price`: Calculates the final, tax, and total amounts for the course.
            - `place_order`: Places the order while deducting the balance from the user.
    """
    def __init__(self, user, course_title, coupon_code=None):
        self.user = user
        self.course = get_object_or_404(Course, title=course_title)
        self.coupon = Coupon.objects.filter(code=coupon_code).first() if coupon_code else None

        if self.course.instructor == self.user:
            raise ValueError("You cannot order your own course.")
        if Order.objects.filter(user=self.user, course=self.course).exists():
            raise ValueError("You have already ordered this course.")
        if self.coupon:
            self.validate_coupon()

    def validate_coupon(self):
        """
        Validate the coupon for the selected course and check its rules.
        """
        # Ensure the coupon is active and not expired
        if not self.coupon.is_valid():
            raise ValueError("The coupon is either expired or inactive.")
        if self.coupon.min_order_value and self.course.price < self.coupon.min_order_value:
            raise ValueError(f"The course price must exceed {self.coupon.min_order_value:.2f} to use this coupon.")

    def calculate_price(self):
        """
        Calculate the final price, tax, and total amount after applying the coupon discount.
        """
        # Calculate discount or set it to 0 if no coupon is provided
        discount_percentage = self.coupon.discount_percentage if self.coupon else 0

        final_price, tax_amount, total_amount = calculate_final_price(
            base_price=self.course.price,
            discount_percentage=discount_percentage,
            tax_percentage=5
        )
        return final_price, tax_amount, total_amount

    def place_order(self):
        """
        Place the order after validating the user's balance and applying discounts.
        """
        final_price, tax_amount, total_amount = self.calculate_price()
        account_balance = get_object_or_404(AccountBalance, user=self.user)

        if account_balance.balance < total_amount:
            raise ValueError("Insufficient balance to place this order.")

        account_balance.subtract_balance(total_amount)

        return Order.objects.create(
            user=self.user,
            course=self.course,
            coupon=self.coupon,
            amount=final_price,
            tax_amount=tax_amount,
        )
