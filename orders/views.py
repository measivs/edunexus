from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Order, Coupon
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsCourseOwner
from .serializers import OrderSerializer, CreateOrderSerializer, CouponCreateSerializer
from .services.order_service import OrderService
from .signals import order_success
from .tasks import send_order_confirmation_email


class OrderViewSet(ModelViewSet):
    """
        ViewSet for managing user orders.

        Provides create, retrieve, update, and delete functionalities
        for orders associated with the authenticated user.

        Permissions:
            - Requires authentication.

        Actions:
            - Uses `CreateOrderSerializer` when creating an order.
            - Uses `OrderSerializer` for other actions.

        - Filters orders to only include those created by the logged-in user.
        - Automatically sends a confirmation email and signals order success on order creation.
    """
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related(
            'user',
            'course',
            'coupon'
        )

    def create(self, request, *args, **kwargs):
        try:
            order_service = OrderService(
                user=request.user,
                course_title=request.data.get("course_title"),
                coupon_code=request.data.get("coupon_code"),
            )
            order = order_service.place_order()
            order_success.send(sender=Order, user=request.user, course=order.course)

            send_order_confirmation_email.delay(order.id, request.user.email)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CouponViewSet(ModelViewSet):
    """
    ViewSet for instructors to manage coupons.

    Permissions:
        - Requires authentication and checks for instructor ownership.

    Actions:
        - Allows instructors to create, retrieve, update, and delete coupons.
        - Filters the queryset to include only the coupons created by the logged-in instructor.
    """
    permission_classes = [IsAuthenticated, IsCourseOwner]
    serializer_class = CouponCreateSerializer

    def get_queryset(self):
        return Coupon.objects.filter(creator=self.request.user).prefetch_related('courses')
