from django.db import models
from sales.models import Sale

class Product(models.Model):
    product_code = models.CharField(max_length=100, verbose_name='Product Code')
    product_name = models.CharField(max_length=255, verbose_name='Product')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    create_date = models.DateField(verbose_name='Create Date', auto_now_add=True)
    update_date = models.DateField(verbose_name='Update Date', null=True, blank=True)
    
    def __str__(self):
        return self.product_name
    
    def sell(self, quantity_sold):
        if quantity_sold <= 0:
            raise ValueError("Quantity sold must be a positive integer")
        if quantity_sold > self.quantity:
            raise ValueError("Not enough quantity available for sale")
        
        total_price = quantity_sold * self.price
        
        # Verificar se existe uma venda para este produto
        sale = Sale.objects.filter(product=self).first()
        
        if sale:
            # Atualizar a venda existente
            sale.quantity_sold += quantity_sold
            sale.total_price += total_price
            sale.save()
        else:
            # Criar uma nova instância de Sale e salvá-la no banco de dados
            sale = Sale.objects.create(
                product=self,
                quantity_sold=quantity_sold,
                total_price=total_price
            )
        
        # Atualizar a quantidade do produto
        self.quantity -= quantity_sold
        self.save()
        
        return sale
