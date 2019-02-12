from django.contrib.auth.models import User

from estoque.models import (CategoriaProduto, MovimentoEstoque, Produto,
                            SubCategoriaProduto, Medida, Local)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


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


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class MovimentoEstoqueSerializer(serializers.ModelSerializer):

    produto = ProdutoSerializer(read_only="yes")
    usuario = UsuarioSerializer(read_only="yes")
    saldo = SerializerMethodField()

    class Meta:
        model = MovimentoEstoque
        fields = '__all__'

    def get_saldo(self, obj):

        if obj.tipo_movimento == 'entrada':
            return obj.saldo_anterior + obj.quantidade

        elif obj.tipo_movimento == 'saida':
            return obj.saldo_anterior - obj.quantidade

    def create(self, validated_data):

        produto_id = self.context['request'].data['produto']
        usuario_id = self.context['request'].data['usuario']

        data = validated_data['data']
        tipo = validated_data['tipo_movimento']
        motivo = validated_data.get('motivo', '')
        quantidade = validated_data['quantidade']
        observacao = validated_data.get('observacao', '')

        produto = Produto.objects.get(pk=produto_id)
        usuario = User.objects.get(pk=usuario_id)

        if quantidade > produto.estoque and tipo == 'saida':
            raise serializers.ValidationError('A quantidade informada é superior ao estoque')

        movimento = MovimentoEstoque.objects.create(
            data=data,
            produto=produto,
            tipo_movimento=tipo,
            motivo=motivo,
            quantidade=quantidade,
            saldo_anterior=produto.estoque,
            observacao=observacao,
            usuario=usuario
        )

        if tipo == 'entrada':
            produto.estoque += quantidade
            produto.save()

        elif tipo == 'saida':
            produto.estoque -= quantidade
            produto.save()

        movimento.save()
        return movimento

