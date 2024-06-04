class Frete:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, distancia):
        if self.successor:
            return self.successor.handle(distancia)
        return None

class FreteAte2Km(Frete):
    def handle(self, distancia):
        if 0 <= distancia <= 2:
            return 2 * distancia
        else:
            return super().handle(distancia)

class FreteAte5Km(Frete):
    def handle(self, distancia):
        if 2 < distancia <= 5:
            return 2.5 * distancia
        else:
            return super().handle(distancia)

class FreteAcimaDe5Km(Frete):
    def handle(self, distancia):
        if distancia > 5:
            return None
        else:
            return super().handle(distancia)

# Gera cadeia de responsabilidades
def calculaFrete(distancia):
    frete_chain = FreteAte2Km(FreteAte5Km(FreteAcimaDe5Km()))
    return frete_chain.handle(distancia)
