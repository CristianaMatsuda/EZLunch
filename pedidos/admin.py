from django.contrib import admin

from .models import Categoria, Conteudo, Marmita, Item, Pedido, Tamanho
# Mostra os logs no admin mas nao tem filtro por data e queria fazer algumas modificaoes na visualizacao
# from django.contrib.admin.models import LogEntry
# admin.site.register(LogEntry)

class ConteudoInline(admin.TabularInline):
    model = Conteudo
    extra = 3

class CategoriaAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["question_text"]}),
    #     ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    # ]
    inlines = [ConteudoInline]
    # list_display = ["question_text", "pub_date", "was_published_recently"]
    # list_filter = ["pub_date"]
    # search_fields = ["pub_date"]

# class MarmitaInline(admin.TabularInline):
#     model = Marmita
#     extra = 1

# class ItemAdmin(admin.ModelAdmin):
#     inlines = [MarmitaInline]

# admin.site.register(Question, QuestionAdmin)

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Conteudo)
admin.site.register(Marmita)
admin.site.register(Item)
admin.site.register(Pedido)
admin.site.register(Tamanho)