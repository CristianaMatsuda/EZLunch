from django import forms

from .models import Conteudo

class MarmitaForm(forms.Form):
    TAMANHOS = [
        (None, ''),
        ('P', 'Pequena'),
        ('M', 'Média'),
        ('G', 'Grande')
    ]

    # Gera lista de tuplas das possíveis escolhas para cada Categoria
    def get_choices(queryset):
        choices = [(None, '')]
        for item in queryset:
            choices.append((item.id, item.descricao))
        return choices

    # Busca apenas os conteudos para cada Categoria (usa o iexact para ser case insensitive)
    BASES = get_choices(Conteudo.objects.filter(categoria__descricao__iexact='base'))
    CARNES = get_choices(Conteudo.objects.filter(categoria__descricao__iexact='carne'))
    SALADAS = get_choices(Conteudo.objects.filter(categoria__descricao__iexact='salada'))
    EXTRAS = get_choices(Conteudo.objects.filter(categoria__descricao__iexact='extra'))

    marmita_tipo = forms.ChoiceField(choices=TAMANHOS)
    item_quantidade = forms.IntegerField()
    marmita_base1 = forms.ChoiceField(choices=BASES)
    marmita_base2 = forms.ChoiceField(choices=BASES, required=False)
    marmita_carne1 = forms.ChoiceField(choices=CARNES)
    marmita_carne2 = forms.ChoiceField(choices=CARNES, required=False)
    marmita_salada = forms.ChoiceField(choices=SALADAS)
    marmita_extra = forms.ChoiceField(choices=EXTRAS, required=False)

class FinalizarPedidoForm(forms.Form):
    distancia = forms.DecimalField(max_digits=5, decimal_places=2, label="Distância em km")