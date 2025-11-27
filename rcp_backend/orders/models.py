from django.db import models
from django.conf import settings
from pens.models import Pen, Refill


class Order(models.Model):
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="pending"
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # Option A: Two product relations
    pen = models.ForeignKey(Pen, null=True, blank=True, on_delete=models.SET_NULL)
    refill = models.ForeignKey(Refill, null=True, blank=True, on_delete=models.SET_NULL)

    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.pen:
            product_name = self.pen.name
        elif self.refill:
            product_name = self.refill.name
        else:
            product_name = "Unknown Product"

        return f"{self.quantity} x {product_name}"
