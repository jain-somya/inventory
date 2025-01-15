# inventory/models.py
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal

class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be 10 digits'
            )
        ]
    )
    address = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock_quantity = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def save(self, *args, **kwargs):
        if not self.total_price:
            product_price = Decimal(str(self.product.price))     
            self.total_price = product_price * self.quantity
        super().save(*args, **kwargs)

class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ('In', 'In'),
        ('Out', 'Out')
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    movement_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)