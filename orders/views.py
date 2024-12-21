from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Order, Coupon
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsCourseOwner
from .serializers import OrderSerializer, CreateOrderSerializer, CouponCreateSerializer
from .services.order_service import OrderService


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Use CreateOrderSerializer for the 'create' action, and
        OrderSerializer for all other actions (e.g., list, retrieve, etc.).
        """
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        """
        Limit orders to those created by the authenticated user.
        """
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            order_service = OrderService(
                user=request.user,
                course_title=request.data.get("course_title"),
                coupon_code=request.data.get("coupon_code"),
            )
            order = order_service.place_order()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CouponViewSet(ModelViewSet):
    """
    Viewset for instructors to manage their coupons.
    """
    permission_classes = [IsAuthenticated, IsCourseOwner]
    serializer_class = CouponCreateSerializer

    def get_queryset(self):
        """
        Restrict query to coupons created by the logged-in instructor.
        """
        return Coupon.objects.filter(creator=self.request.user)

