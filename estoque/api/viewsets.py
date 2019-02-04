from rest_framework import filters
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from estoque.api.serializers import CategoriaProdutoSerializer
from estoque.api.serializers import SubCategoriaProdutoSerializer
from estoque.api.serializers import ProdutoSerializer
from estoque.api.serializers import MovimentoEstoqueSerializer
from rest_framework.response import Response

from estoque.models import CategoriaProduto
from estoque.models import SubCategoriaProduto
from estoque.models import Produto
from estoque.models import MovimentoEstoque


class CategoriaViewSet(viewsets.ModelViewSet):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (DjangoModelPermissions,)

    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nome', 'descricao')


class SubCategoriaViewSet(viewsets.ModelViewSet):

    #authentication_classes = (JWTAuthentication, )
    #permission_classes = (DjangoModelPermissions,)

    queryset = SubCategoriaProduto.objects.all()
    serializer_class = SubCategoriaProdutoSerializer
    search_fields = ('nome', 'descricao')


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_fields = ('codigo', 'descricao', 'local')


class MovimentoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentoEstoque.objects.all()
    serializer_class = MovimentoEstoqueSerializer
    filter_fields = ('data', 'produto', 'tipo_movimento')
