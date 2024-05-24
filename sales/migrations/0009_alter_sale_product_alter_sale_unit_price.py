# Generated by Django 5.0.3 on 2024-05-24 03:36

import django.db.models.query
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_id'),
        ('sales', '0008_alter_sale_product_alter_sale_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.query.prefetch_related_objects, to='product.product'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='unit_price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.query.prefetch_related_objects, related_name='unit_price_sales', to='product.product', verbose_name='Unit Price'),
        ),
    ]
