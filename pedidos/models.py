from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Conteudo(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class Marmita(models.Model):
    TAMANHOS = [
        ('P', 'Pequena'),
        ('M', 'Média'),
        ('G', 'Grande')
    ]

    tamanho = models.CharField(max_length=1, choices=TAMANHOS)
    base1 = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    base2 = models.ForeignKey(Conteudo, on_delete=models.CASCADE, blank=True)
    carne1 = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    carne2 = models.ForeignKey(Conteudo, on_delete=models.CASCADE, blank=True)
    salada = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    extra = models.ForeignKey(Conteudo, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Marmita {self.get_tamanho_display()}"

class Pedido(models.Model):
    vl_frete = models.DecimalField(max_digits=10, decimal_places=2)
    vl_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    # Mudar para cliente
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class Item(models.Model):
    quantidade = models.IntegerField
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    marmita = models.ForeignKey(Marmita, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantidade} marmita(s) {self.marmita}"