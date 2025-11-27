from django.db import models

class Pen(models.Model):
    CATEGORY_CHOICES = [
        ('fountain', 'Fountain Pen'),
        ('ballpoint', 'Ballpoint Pen'),
        ('rollerball', 'Rollerball Pen'),
        ('gel', 'Gel Pen'),
        ('ink', 'Ink Pen'),
        ('vintage', 'Vintage Pen'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='pens/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_vintage = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    in_stock = models.BooleanField(default=True)  # Auto updated

    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Refill(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ("ballpoint", "Ballpoint"),
            ("gel", "Gel"),
            ("roller", "Roller"),
            ("fountain", "Fountain Ink Cartridge"),
            ("others", "Others"),
        ],
        default="ballpoint",
    )
    size = models.CharField(max_length=100)
    compatible_pen = models.CharField(max_length=150, blank=True, null=True)
    ink_color = models.CharField(max_length=30, default="blue")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="refills/", blank=True, null=True)
    in_stock = models.BooleanField(default=True)  # Auto updated
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category} ({self.size}, {self.ink_color})"
