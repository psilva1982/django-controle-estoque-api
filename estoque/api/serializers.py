from estoque.models import (CategoriaProduto, MovimentoEstoque, Produto,
                            SubCategoriaProduto, Medida, Local)
from rest_framework import serializers


class CategoriaProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoriaProduto
        fields = '__all__'


class SubCategoriaProdutoSerializer(serializers.ModelSerializer):

    categoria = CategoriaProdutoSerializer(read_only=True)

    class Meta:
        model = SubCategoriaProduto
        fields = '__all__'

    def create(self, validated_data):

        categoria_id = self.context['request'].data['categoria']
        nome = validated_data['nome']
        descricao = validated_data.get('descricao', '')

        categoria = CategoriaProduto.objects.get(pk=categoria_id)

        sub = SubCategoriaProduto.objects.create(
            nome=nome,
            descricao=descricao,
            categoria=categoria
        )

        sub.save()
        return sub

    def update(self, instance, validated_data):

        categoria_id = self.context['request'].data['categoria']
        nome = validated_data['nome']
        descricao = validated_data.get('descricao', '')
        categoria = CategoriaProduto.objects.get(pk=categoria_id)

        subcategoria = instance

        subcategoria.categoria = categoria
        subcategoria.nome = nome
        subcategoria.descricao = descricao

        subcategoria.save()
        return subcategoria


class MedidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medida
        fields = '__all__'


class LocalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Local
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):

    subcategoria = SubCategoriaProdutoSerializer(read_only=True)
    medida = MedidaSerializer(read_only=True)
    local = LocalSerializer(read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

    def create(self, validated_data):

        subcategoria_id = self.context['request'].data['subcategoria']
        medida_id = self.context['request'].data['medida']
        local_id = self.context['request'].data['local']

        codigo = validated_data['codigo']
        descricao = validated_data['descricao']
        minimo = validated_data['minimo']

        subcategoria = SubCategoriaProduto.objects.get(pk=subcategoria_id)
        medida = Medida.objects.get(pk=medida_id)
        local = Local.objects.get(pk=local_id)

        produto = Produto.objects.create(
            codigo=codigo,
            descricao=descricao,
            subcategoria=subcategoria,
            medida=medida,
            minimo=minimo,
            local=local
        )

        produto.save()
        return produto

    def update(self, instance, validated_data):

        subcategoria_id = self.context['request'].data['subcategoria']
        medida_id = self.context['request'].data['medida']
        local_id = self.context['request'].data['local']

        codigo = validated_data['codigo']
        descricao = validated_data['descricao']
        minimo = validated_data['minimo']

        subcategoria = SubCategoriaProduto.objects.get(pk=subcategoria_id)
        medida = Medida.objects.get(pk=medida_id)
        local = Local.objects.get(pk=local_id)

        produto = instance

        produto.codigo = codigo
        produto.descricao = descricao
        produto.subcategoria = subcategoria
        produto.medida = medida
        produto.minimo = minimo
        produto.local = local

        produto.save()
        return produto


class MovimentoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentoEstoque
        fields = '__all__'

