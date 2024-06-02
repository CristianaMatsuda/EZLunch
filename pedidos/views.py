from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.forms import formset_factory
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages

from .models import Categoria, Conteudo, Marmita, Item, Pedido
from .marmitaBuilder import MarmitaBuilder
from .forms import MarmitaForm, FinalizarPedidoForm
from .frete import calculaFrete

class IndexView(LoginRequiredMixin, generic.ListView):
    # Melhorar para filtrar por status e colocar um paginador

    template_name = "pedidos/index.html"
    context_object_name = "latest_pedido_list"
    paginate_by = 5

    def get_queryset(self):
        """Retorna os ultimos pedidos incluidos do usuario conectado, exceto os pedidos cancelados."""
        return Pedido.objects.filter(~Q(status='C'), cliente_id=self.request.user.id)\
                             .select_related('cliente')\
                             .prefetch_related('item_set__marmita')\
                             .order_by("-data_inclusao")
class DetailView(LoginRequiredMixin, generic.DetailView):
    # Melhorar para nao dar pagina de erro quando nao tiver o indice para aquele usuario

    model = Pedido
    template_name = "pedidos/detail.html"
    context_object_name = "item_list"

    def get_queryset(self):
        """Retorna os ultimos pedidos incluidos do usuario conectado."""
        return Pedido.objects.filter(cliente_id=self.request.user.id)\
                             .select_related('cliente')\
                             .prefetch_related('item_set__marmita__base1',
                                               'item_set__marmita__base2',
                                               'item_set__marmita__carne1',
                                               'item_set__marmita__carne2',
                                               'item_set__marmita__salada',
                                               'item_set__marmita__extra')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens'] = self.object.item_set.all()
        return context

@login_required
def adicionar_marmita(request):
    if request.method == 'POST':
        form = MarmitaForm(request.POST)
        if form.is_valid():
            '''
             Marmita Pequena: Até duas bases + 1 carne + salada
             Marmita Média:   Até duas bases + 2 carne + salada
             Marmita Grande:  Até duas bases + 2 carne + salada + extra
            '''
            marmita_builder = MarmitaBuilder()

            # Constroi a marmita usando builder para incluir os itens mínimos
            marmita_builder.define_tamanho(form.cleaned_data['marmita_tipo'])\
                           .adiciona_base(form.cleaned_data['marmita_base1'])\
                           .adiciona_carne(form.cleaned_data['marmita_carne1'])\
                           .adiciona_salada(form.cleaned_data['marmita_salada'])

            # Verifica se os demais itens foram preenchidos para incluir na marmita
            if form.cleaned_data['marmita_base2']:
                marmita_builder.adiciona_base(form.cleaned_data['marmita_base2'])

            if form.cleaned_data['marmita_carne2']:
                marmita_builder.adiciona_carne(form.cleaned_data['marmita_carne2'])

            if form.cleaned_data['marmita_extra']:
                marmita_builder.adiciona_extra(form.cleaned_data['marmita_extra'])

            marmita = marmita_builder.constroi_marmita()
            marmita.save()

            # Verifica se existe um pedido em aberto, senao cria
            pedido, _ = Pedido.objects.get_or_create(
                cliente=request.user,
                status='A',
                defaults={'vl_frete': 0, 'distancia': 0, 'vl_frete': 0, 'vl_pedido': 0}
            )

            item = Item(pedido=pedido, marmita=marmita, quantidade=form.cleaned_data['item_quantidade'])
            item.save()

            messages.success(request, 'Marmita adicionada ao carrinho.')
            return redirect('pedidos:visualizar-carrinho')

    else:
        form = MarmitaForm()

    return render(request, 'pedidos/adicionar_marmita.html', {'form': form})

@login_required
def remover_marmita(request, item_id):
    item = get_object_or_404(Item, id=item_id, pedido__cliente=request.user, pedido__status='A')
    item.delete()
    messages.success(request, 'Marmita removida do carrinho.')
    return redirect('pedidos:visualizar-carrinho')

@login_required
def visualizar_carrinho(request):
    # Verifica se existe um pedido em aberto para o usuario, senao cria
    pedido, _ = Pedido.objects.get_or_create(
        cliente=request.user,
        status='A',
        defaults={'vl_frete': 0, 'distancia': 0, 'vl_frete': 0, 'vl_pedido': 0}
    )
    itens = pedido.item_set.all()

    return render(request, 'pedidos/visualizar_carrinho.html', {'pedido': pedido, 'itens': itens})

@login_required
def fechar_pedido(request):

    def calcular_valor(pedido):
        valor = 0
        for item in pedido.item_set.all():
            valor += item.quantidade * item.marmita.tamanho.preco
        return valor

    # Verifica se existe um pedido em aberto, senao cria
    pedido, _ = Pedido.objects.get_or_create(
        cliente=request.user,
        status='A',
        defaults={'vl_frete': 0, 'distancia': 0, 'vl_frete': 0, 'vl_pedido': 0}
    )

    if request.method == 'POST':
        form = FinalizarPedidoForm(request.POST)
        if form.is_valid():
            distancia = form.cleaned_data['distancia']

            # Calcular o valor do frete com base na distância
            valor_frete = calculaFrete(distancia)
            if not valor_frete:
                messages.error(request, "Distância fora da área de entrega.")
                return redirect('pedidos:fechar-pedido')

            pedido.vl_frete = valor_frete
            pedido.vl_pedido = calcular_valor(pedido)
            pedido.status = 'P'
            pedido.save()
            messages.success(request, 'Pedido finalizado com sucesso.')
            return redirect('pedidos:index')
    else:
        form = FinalizarPedidoForm()

    return render(request, 'pedidos/finalizar_pedido.html', {'form': form, 'pedido': pedido})

@login_required
def cancelar_pedido(request, pedido_id):
    # Somente pedidos pendentes podem ser cancelados
    pedido = get_object_or_404(Pedido, cliente=request.user, pk=pedido_id, status='P')

    pedido.status = 'C'
    pedido.data_cancelado = timezone.now()
    pedido.save()
    messages.success(request, 'Pedido cancelado com sucesso.')
    return redirect('pedidos:index')

