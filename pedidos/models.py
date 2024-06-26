from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin

class Categoria(DirtyFieldsMixin, models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Conteudo(DirtyFieldsMixin, models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Tamanho(DirtyFieldsMixin, models.Model):
    codigo = models.CharField(max_length=1, primary_key=True)
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descricao

class Marmita(DirtyFieldsMixin, models.Model):
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    base1 = models.ForeignKey(Conteudo, related_name='base1', on_delete=models.CASCADE)
    base2 = models.ForeignKey(Conteudo, related_name='base2', on_delete=models.CASCADE, blank=True, null=True)
    carne1 = models.ForeignKey(Conteudo, related_name='carne1', on_delete=models.CASCADE)
    carne2 = models.ForeignKey(Conteudo, related_name='carne2', on_delete=models.CASCADE, blank=True, null=True)
    salada = models.ForeignKey(Conteudo, related_name='salada', on_delete=models.CASCADE)
    extra = models.ForeignKey(Conteudo, related_name='extra', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.tamanho}"

class Pedido(DirtyFieldsMixin, models.Model):
    STATUS = [
        ('A', 'ABERTO'),
        ('P', 'PENDENTE'),
        ('E', 'ENTREGUE'),
        ('C', 'CANCELADO')
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    distancia = models.DecimalField(max_digits=10, decimal_places=2)
    vl_frete = models.DecimalField(max_digits=10, decimal_places=2)
    vl_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS, default='A')
    data_inclusao = models.DateTimeField("Data Inclusão", default=timezone.now)
    data_cancelado = models.DateTimeField("Data Cancelamento", blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id} - Cliente {self.cliente.username}"

class Item(DirtyFieldsMixin, models.Model):
    quantidade = models.IntegerField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    marmita = models.ForeignKey(Marmita, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantidade} marmita(s) {self.marmita}"