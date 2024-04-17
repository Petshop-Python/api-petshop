from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=100, verbose_name='Product Code')
    product_name = models.CharField(max_length=255, verbose_name='Product')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.product_name


