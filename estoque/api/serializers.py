from rest_framework import serializers

from estoque.models import CategoriaProduto
from estoque.models import SubCategoriaProduto
from estoque.models import Produto
from estoque.models import MovimentoEstoque

class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CategoriaProduto
        fields = '__all__'


class SubCategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriaProduto
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'codigo', 'descricao', 'subcategoria', 'minimo')

class MovimentoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentoEstoque
        fields = '__all__'