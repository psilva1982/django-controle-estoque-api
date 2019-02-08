
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from estoque.api.serializers import (CategoriaProdutoSerializer,
                                     LocalSerializer,
                                     MedidaSerializer,
                                     MovimentoEstoqueSerializer,
                                     ProdutoSerializer,
                                     SubCategoriaProdutoSerializer)
from estoque.models import (CategoriaProduto, Local, Medida, MovimentoEstoque,
                            Produto, SubCategoriaProduto)
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


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

    authentication_classes = (JWTAuthentication, )
    permission_classes = (DjangoModelPermissions,)

    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    filter_fields = ('local', 'subcategoria', 'medida')
    search_fields = ('codigo', 'descricao',)

    @action(methods=['get'], detail=False)
    def estatistica(self, request):
        produtos = Produto.objects.count()
        
        retorno = {
            "total": produtos,
            "total2": produtos,
        } 

        return Response(retorno)


class MovimentoEstoqueViewSet(viewsets.ModelViewSet):

    serializer_class = MovimentoEstoqueSerializer
    queryset = MovimentoEstoque.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend,)


class LocalViewSet(viewsets.ModelViewSet):

    serializer_class = LocalSerializer
    queryset = Local.objects.all()


class MedidaViewSet(viewsets.ModelViewSet):

    serializer_class = MedidaSerializer
    queryset = Medida.objects.all()

class DashBoardView(APIView):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, format=None):
        produtos = Produto.objects.count()
        sem_estoque = Produto.objects.filter(estoque__exact=0).count()
        maior_estoque = Produto.objects.order_by('-estoque')[0]

        print(maior_estoque)

        retorno = {
            "produtos": produtos,
            "sem_estoque": sem_estoque,
            "maior_estoque": maior_estoque.descricao
        }

        return Response(retorno)
