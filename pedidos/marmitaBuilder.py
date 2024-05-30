from django.shortcuts import get_object_or_404
from .models import Marmita, Conteudo

class MarmitaBuilder:
    def __init__(self):
        self.tamanho = None
        self.base1 = None
        self.base2 = None
        self.carne1 = None
        self.carne2 = None
        self.salada = None
        self.extra = None

    def define_tamanho(self, tamanho):
        self.tamanho = tamanho
        return self

    def adiciona_base(self, base):
        # Busca a instancia do Conteudo de acordo com o que foi selecionado
        base = get_object_or_404(Conteudo, pk=base)

        if self.base1 is None:
            self.base1 = base
        elif self.base2 is None:
            self.base2 = base
        else:
            raise ValueError("Já foram adicionadas duas bases.")
        return self

    def adiciona_carne(self, carne):
        # Busca a instancia do Conteudo de acordo com o que foi selecionado
        carne = get_object_or_404(Conteudo, pk=carne)

        if self.carne1 is None:
            self.carne1 = carne
        elif self.carne2 is None:
            self.carne2 = carne
        else:
            raise ValueError("Já foram adicionadas duas carnes.")
        return self

    def adiciona_salada(self, salada):
        # Busca a instancia do Conteudo de acordo com o que foi selecionado
        salada = get_object_or_404(Conteudo, pk=salada)

        self.salada = salada
        return self

    def adiciona_extra(self, extra):
        # Busca a instancia do Conteudo de acordo com o que foi selecionado
        extra = get_object_or_404(Conteudo, pk=extra)

        self.extra = extra
        return self

    def constroi_marmita(self):
        if not self.tamanho:
            raise ValueError("O tamanho da marmita deve ser definido.")
        if not self.base1:
            raise ValueError("Pelo menos uma base deve ser adicionada.")
        if not self.carne1:
            raise ValueError("Pelo menos uma carne deve ser adicionada.")
        if not self.salada:
            raise ValueError("A salada deve ser adicionada.")

        return Marmita(
            tamanho=self.tamanho,
            base1=self.base1,
            base2=self.base2,
            carne1=self.carne1,
            carne2=self.carne2,
            salada=self.salada,
            extra=self.extra
        )
