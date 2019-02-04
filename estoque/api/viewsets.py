from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from estoque.api.serializers import CategoriaProdutoSerializer
from estoque.api.serializers import SubCategoriaProdutoSerializer
from estoque.api.serializers import ProdutoSerializer
from estoque.api.serializers import MovimentoEstoqueSerializer

from estoque.models import CategoriaProduto
from estoque.models import SubCategoriaProduto
from estoque.models import Produto
from estoque.models import MovimentoEstoque

class CategoriaViewSet(viewsets.ModelViewSet):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAdminUser,)

    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer
    filter_fields = ('nome',)

class SubCategoriaViewSet(viewsets.ModelViewSet):
    queryset = SubCategoriaProduto.objects.all()
    serializer_class = SubCategoriaProdutoSerializer 
    filter_fields = ('nome',)

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_fields = ('codigo', 'descricao', 'local')

class MovimentoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentoEstoque.objects.all()
    serializer_class = MovimentoEstoqueSerializer
    filter_fields = ('data', 'produto', 'tipo_movimento')