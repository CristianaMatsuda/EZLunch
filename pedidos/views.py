from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.forms import formset_factory

# from django.contrib.auth.models import User
from .models import Categoria, Conteudo, Marmita, Item, Pedido
from .marmitaBuilder import MarmitaBuilder
from .forms import MarmitaForm, MarmitaFormSet

class IndexView(generic.ListView):
    # melhorar para filtrar por status e colocar um paginador

    template_name = "pedidos/index.html"
    context_object_name = "latest_pedido_list"
    paginate_by = 5

    def get_queryset(self):
        """Retorna os ultimos pedidos incluidos do usuario conectado."""
        return Pedido.objects.filter(cliente_id=self.request.user.id)\
                             .select_related('cliente')\
                             .prefetch_related('item_set__marmita')\
                             .order_by("-data_inclusao")
        # return Pedido.objects.select_related('item', 'marmita').filter(cliente_id=self.request.user.id).order_by("-data_inclusao")


class DetailView(generic.DetailView):
    # Melhorar para nao dar pagina de erro quando nao tiver o indice para aquele usuario

    model = Pedido
    template_name = "pedidos/detail.html"
    context_object_name = "item_list"

    def get_queryset(self):
        """Return os ultimos pedidos incluidos do usuario conectado."""
        # return Pedido.objects.filter(cliente_id=self.request.user.id)\
        #     .select_related('cliente')\
        #     .prefetch_related('item_set__marmita')\
        #     .order_by("-data_inclusao")
        # return Item.objects.select_related('marmita')\
        #                    .prefetch_related('marmita__base1', 'marmita__base2', 'marmita__carne1', 'marmita__carne2', 'marmita__salada', 'marmita__extra')
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

def incluir_pedido(request):
    # if request.method == 'POST':
    #     form = MarmitaForm(request.POST)
    #     if form.is_valid():
    #         marmita_builder = MarmitaBuilder()
    #         marmita_tipo = form.cleaned_data['marmita_tipo']
    #         if marmita_tipo == 'P':
    #             marmita = marmita_builder.define_tamanho(marmita_tipo)\
    #                                      .adiciona_base(form.cleaned_data['marmita_base1'])\
    #                                      .adiciona_base(form.cleaned_data['marmita_base2'])\
    #                                      .adiciona_carne(form.cleaned_data['marmita_carne1'])\
    #                                      .adiciona_salada(form.cleaned_data['marmita_salada'])\
    #                                      .constroi_marmita()
    #         elif marmita_tipo == 'M':
    #             marmita = marmita_builder.define_tamanho(marmita_tipo)\
    #                                      .adiciona_base(form.cleaned_data['marmita_base1'])\
    #                                      .adiciona_base(form.cleaned_data['marmita_base2'])\
    #                                      .adiciona_carne(form.cleaned_data['marmita_carne1'])\
    #                                      .adiciona_carne(form.cleaned_data['marmita_carne2'])\
    #                                      .adiciona_salada(form.cleaned_data['marmita_salada'])\
    #                                      .constroi_marmita()
    #         else:
    #             marmita = marmita_builder.define_tamanho(marmita_tipo)\
    #                                      .adiciona_base(form.cleaned_data['marmita_base1'])\
    #                                      .adiciona_base(form.cleaned_data['marmita_base2'])\
    #                                      .adiciona_carne(form.cleaned_data['marmita_carne1'])\
    #                                      .adiciona_carne(form.cleaned_data['marmita_carne2'])\
    #                                      .adiciona_salada(form.cleaned_data['marmita_salada'])\
    #                                      .adiciona_extra(form.cleaned_data['marmita_extra'])\
    #                                      .constroi_marmita()
    #         marmita.save()

    #         pedido = Pedido(marmita=marmita, cliente=request.user, vl_frete=0, vl_pedido=50)
    #         pedido.save()

    #         item = Item(quantidade=form.cleaned_data['item_quantidade'], pedido=pedido, marmita=marmita)
    #         item.save()

    #         return redirect('pedido_sucesso')

    # else:
    #     form = MarmitaForm()

    # return render(request, 'pedidos/pedidos.html', {'form': form})

    MarmitaFormSet = formset_factory(MarmitaForm, extra=1)

    if request.method == 'POST':
        formset = MarmitaFormSet(request.POST)
        if formset.is_valid():
            pedido = Pedido(cliente=request.user, vl_frete=0, vl_pedido=0)
            pedido.save()

            for form in formset:
                if form.cleaned_data:
                    marmita_builder = MarmitaBuilder()
                    marmita_tipo = form.cleaned_data['marmita_tipo']

                    marmita_builder.define_tamanho(marmita_tipo)\
                                .adiciona_base(form.cleaned_data['marmita_base1'])

                    if form.cleaned_data['marmita_base2']:
                        marmita_builder.adiciona_base(form.cleaned_data['marmita_base2'])

                    marmita_builder.adiciona_carne(form.cleaned_data['marmita_carne1'])

                    if form.cleaned_data['marmita_carne2']:
                        marmita_builder.adiciona_carne(form.cleaned_data['marmita_carne2'])

                    marmita_builder.adiciona_salada(form.cleaned_data['marmita_salada'])

                    if form.cleaned_data['marmita_extra']:
                        marmita_builder.adiciona_extra(form.cleaned_data['marmita_extra'])

                    marmita = marmita_builder.constroi_marmita()
                    marmita.save()

                    item = Item(quantidade=form.cleaned_data['item_quantidade'], pedido=pedido, marmita=marmita)
                    item.save()

            return redirect('pedido_sucesso')

    else:
        formset = MarmitaFormSet()

    return render(request, 'pedidos/pedido_form.html', {'formset': formset})