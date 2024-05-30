# Generated by Django 5.0.6 on 2024-05-30 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_pedido_distancia'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='data_cancelado',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data Cancelamento'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('A', 'ABERTO'), ('P', 'PENDENTE'), ('E', 'ENTREGUE'), ('C', 'CANCELADO')], default='A', max_length=1),
        ),
    ]
