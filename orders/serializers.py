from rest_framework import serializers
from courses.models import Course
from .models import Order, Coupon


class OrderSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving order information.

        Includes details like the user, course, coupon, order amount,
        tax amount, and timestamps.

        Read-only fields:
            - User, course, coupon, amount, tax, created_at, and updated_at.
    """
    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    coupon = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "course",
            "coupon",
            "amount",
            "tax_amount",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ("amount", "tax_amount", "user", "created_at", "updated_at")


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating an order.

    Fields:
        - `course_title` (required): The title of the course being purchased.
        - `coupon_code` (optional): A discount code to apply to the order.

    Validations:
        - Ensures the provided course exists.
        - Ensures the coupon is valid and active if provided.
    """
    course_title = serializers.CharField(required=True, help_text="Title of the course to order.")
    coupon_code = serializers.CharField(required=False, allow_blank=True, help_text="Optional discount code.")

    def validate_course_title(self, value):
        if not Course.objects.filter(title=value).exists():
            raise serializers.ValidationError("Invalid course title. The course does not exist.")
        return value

    def validate_coupon_code(self, value):
        if value and not Coupon.objects.filter(code=value, is_active=True).exists():
            raise serializers.ValidationError("Invalid or expired coupon code.")
        return value


class CouponCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating and managing coupons.

        Fields:
            - `code`: Unique code for the coupon.
            - `discount_percentage`: Discount percentage offered by the coupon.
            - `valid_until`: The expiration date of the coupon.
            - `is_active`: Indicates whether the coupon is active.
            - `min_order_value`: The minimum order value required to apply the coupon.
            - `courses`: The list of courses this coupon applies to (optional; default is global).
        Validations:
        - Ensures that the courses being linked to the coupon belong to the logged-in user.
        - Ensures the discount percentage is between 1 and 100.
    """
    courses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        required=False,
        help_text="Courses this coupon applies to. Leave empty to make it a global coupon."
    )

    class Meta:
        model = Coupon
        fields = [
            "code", "discount_percentage", "valid_until", "is_active",
            "min_order_value", "courses"
        ]

    def validate(self, data):
        user = self.context["request"].user

        courses = data.get("courses", [])
        for course in courses:
            if course.instructor != user:
                raise serializers.ValidationError(f"You do not own the course: {course.title}.")

        discount = data.get("discount_percentage", 0)
        if discount <= 0 or discount > 100:
            raise serializers.ValidationError("Discount percentage must be between 1 and 100.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["creator"] = user
        courses = validated_data.pop("courses", [])

        coupon = super().create(validated_data)
        coupon.courses.set(courses)
        return coupon
