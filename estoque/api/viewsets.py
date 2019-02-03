from rest_framework import viewsets
from estoque.api.serializers import CategoriaProdutoSerializer
from estoque.models import CategoriaProduto


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer
