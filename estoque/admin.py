from django.contrib import admin

from estoque.models import MovimentoEstoque, Produto
from estoque.models import CategoriaProduto
from estoque.models import SubCategoriaProduto

class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['data', 'tipo_movimento', 'produto_descricao', 'quantidade']
    autocomplete_fields = ('produto',)
    list_filter = ['produto__subcategoria__categoria']

    def produto_descricao(self, obj):
        return obj.produto.descricao
        
class ProdutoAdmin(admin.ModelAdmin):
    search_fields = ('descricao',)
    list_display = ['codigo', 'descricao', 'subcategoria', 'minimo', 'estoque']
    list_filter = ['subcategoria__categoria']
    exclude = ('estoque',)

class SubCategoriaProdutoAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ['nome', 'categoria'] 
    list_filter = ['categoria']

# Register your models here.
admin.site.register(MovimentoEstoque, MovimentoEstoqueAdmin)
admin.site.register(SubCategoriaProduto, SubCategoriaProdutoAdmin)
admin.site.register(CategoriaProduto)
admin.site.register(Produto, ProdutoAdmin)