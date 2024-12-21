from rest_framework import serializers
from courses.models import Course
from .models import Order, Coupon


class OrderSerializer(serializers.ModelSerializer):
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
    Accepts course_title instead of course_id.
    """
    course_title = serializers.CharField(required=True, help_text="Title of the course to order.")
    coupon_code = serializers.CharField(required=False, allow_blank=True, help_text="Optional discount code.")

    def validate_course_title(self, value):
        """
        Ensure the provided course title refers to an existing course.
        """
        if not Course.objects.filter(title=value).exists():
            raise serializers.ValidationError("Invalid course title. The course does not exist.")
        return value

    def validate_coupon_code(self, value):
        if value and not Coupon.objects.filter(code=value, is_active=True).exists():
            raise serializers.ValidationError("Invalid or expired coupon code.")
        return value


class CouponCreateSerializer(serializers.ModelSerializer):
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
        """
        Ensure that the courses belong to the logged-in instructor.
        """
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
        """
        Automatically set the creator field to the logged-in user.
        """
        user = self.context["request"].user
        validated_data["creator"] = user
        courses = validated_data.pop("courses", [])

        coupon = super().create(validated_data)
        coupon.courses.set(courses)
        return coupon
