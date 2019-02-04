from estoque.models import (CategoriaProduto, MovimentoEstoque, Produto,
                            SubCategoriaProduto)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CategoriaProduto
        fields = '__all__'


class SubCategoriaProdutoSerializer(serializers.ModelSerializer):

    categoria = CategoriaProdutoSerializer()
    class Meta:
        model = SubCategoriaProduto
        fields = '__all__'

    def create(self, validated_data):
        cat = validated_data['categoria']
        del(validated_data['categoria'])

        sub = SubCategoriaProduto.objects.create(
            nome = validated_data['nome'],
            descricao = validated_data['descricao'],
            categoria = cat.id
        )

        sub.save()

        return sub

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'codigo', 'descricao', 'subcategoria', 'minimo')


class MovimentoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentoEstoque
        fields = '__all__'
