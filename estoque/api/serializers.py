from rest_framework import serializers

from estoque.models import CategoriaProduto


class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CategoriaProduto
        fields = '__all__'

