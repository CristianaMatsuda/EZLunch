# Generated by Django 5.0.6 on 2024-06-02 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0008_tamanho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marmita',
            name='tamanho',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.tamanho'),
        ),
    ]