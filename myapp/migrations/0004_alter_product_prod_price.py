# Generated by Django 5.1.2 on 2024-12-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]