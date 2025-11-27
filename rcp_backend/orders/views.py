from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Order
from .serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]  # user must be logged in

    def post(self, request):
        serializer = OrderSerializer(
            data=request.data, 
            context={"request": request}
        )

        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    "message": "Order created successfully",
                    "order_id": order.id,
                    "total_amount": order.total_amount,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = OrderSerializer(order)
        return Response(serializer.data)
