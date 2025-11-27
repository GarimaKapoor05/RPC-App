from rest_framework import serializers
from django.shortcuts import get_object_or_404
from decimal import Decimal
from .models import Order, OrderItem
from pens.models import Pen, Refill


class OrderItemSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_type",
            "product_name",
            "product_image",
            "quantity",
            "price_at_purchase",
        ]

    def get_product_type(self, obj):
        return "pen" if obj.pen else "refill"

    def get_product_name(self, obj):
        return obj.pen.name if obj.pen else obj.refill.name

    def get_product_image(self, obj):
        if obj.pen:
            return obj.pen.image.url if obj.pen.image else None
        if obj.refill:
            return obj.refill.image.url if obj.refill.image else None
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_amount",
            "payment_status",
            "created_at",
            "items",
        ]
        read_only_fields = ["id", "payment_status", "created_at", "items"]

    def create(self, validated_data):
        user = self.context["request"].user
        cart_items = self.context["request"].data.get("cart_items", [])

        if not cart_items:
            raise serializers.ValidationError("Cart cannot be empty.")

        order = Order.objects.create(user=user)
        total_amount = Decimal("0.00")

        for item in cart_items:
            product_type = item.get("type")
            product_id = item.get("id")
            quantity = int(item.get("quantity", 1))

            if product_type not in ["pen", "refill"]:
                raise serializers.ValidationError("Invalid product type.")

            model = Pen if product_type == "pen" else Refill
            product = get_object_or_404(model, id=product_id)

            # Check stock
            if product.quantity < quantity:
                raise serializers.ValidationError(
                    f"Only {product.quantity} left in stock for {product.name}."
                )

            # Deduct stock
            product.quantity -= quantity
            product.in_stock = product.quantity > 0
            product.save()

            # Price (sale or regular)
            price_used = product.sale_price if getattr(product, 'on_sale', False) and product.sale_price else product.price

            OrderItem.objects.create(
                order=order,
                pen=product if product_type == "pen" else None,
                refill=product if product_type == "refill" else None,
                quantity=quantity,
                price_at_purchase=price_used,
            )

            total_amount += Decimal(price_used) * quantity

        order.total_amount = total_amount
        order.save()

        return order
