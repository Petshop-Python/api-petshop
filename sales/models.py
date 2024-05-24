from django.db import models
from django.utils import timezone

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    unit_price = models.ForeignKey('product.Product',on_delete=models.CASCADE, related_name='unit_price_sales', verbose_name="Unit Price",null=True)
    quantity_sold = models.PositiveIntegerField(verbose_name='Quantity Sold')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Price')
    sale_date = models.DateField(verbose_name='Sale Date', default=timezone.now)
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)
    
    def __str__(self):
        return f"Sale of {self.quantity_sold} units of {self.product.product_name} on {self.sale_date}"
