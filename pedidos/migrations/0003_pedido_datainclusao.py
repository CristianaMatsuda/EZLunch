# Generated by Django 5.0.6 on 2024-05-26 00:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedido_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='dataInclusao',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 26, 0, 42, 31, 368111, tzinfo=datetime.timezone.utc), verbose_name='Data Inclusão'),
        ),
    ]
