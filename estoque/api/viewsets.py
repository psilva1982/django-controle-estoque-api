from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from estoque.api.serializers import CategoriaProdutoSerializer
from estoque.api.serializers import SubCategoriaProdutoSerializer
from estoque.api.serializers import ProdutoSerializer
from estoque.api.serializers import MovimentoEstoqueSerializer
from estoque.api.serializers import LocalSerializer
from estoque.api.serializers import MedidaSerializer

from estoque.models import CategoriaProduto
from estoque.models import SubCategoriaProduto
from estoque.models import Produto
from estoque.models import Local
from estoque.models import Medida
from estoque.models import MovimentoEstoque


class CategoriaViewSet(viewsets.ModelViewSet):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (DjangoModelPermissions,)

    serializer_class = CategoriaProdutoSerializer
    queryset = CategoriaProduto.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('nome', 'descricao')


class SubCategoriaViewSet(viewsets.ModelViewSet):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (DjangoModelPermissions,)

    serializer_class = SubCategoriaProdutoSerializer
    queryset = SubCategoriaProduto.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    filter_fields = ('categoria',)
    search_fields = ('nome',)


class ProdutoViewSet(viewsets.ModelViewSet):

    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    filter_fields = ('local', 'subcategoria', 'medida')
    search_fields = ('nome', 'codigo', 'descricao',)


class MovimentoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentoEstoque.objects.all()
    serializer_class = MovimentoEstoqueSerializer
    filter_fields = ('data', 'produto', 'tipo_movimento')


class LocalViewSet(viewsets.ModelViewSet):

    serializer_class = LocalSerializer
    queryset = Local.objects.all()


class MedidaViewSet(viewsets.ModelViewSet):

    serializer_class = MedidaSerializer
    queryset = Medida.objects.all()

