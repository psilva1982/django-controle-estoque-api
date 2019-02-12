from django.db.models import Q
from django.db.models import Sum

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
from rest_framework.permissions import IsAuthenticated
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

    @action(methods=['get'], detail=True)
    def estoque(self, request, pk=None):
        produto = self.get_object()

        return Response(produto.estoque)


class MovimentoEstoqueViewSet(viewsets.ModelViewSet):

    serializer_class = MovimentoEstoqueSerializer
    queryset = MovimentoEstoque.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    filter_fields = ('produto', 'tipo_movimento', 'data')

    def destroy(self, request, *args, **kwargs):

        movimento = self.get_object()
        produto = movimento.produto

        if movimento.tipo_movimento == 'entrada':
            produto.estoque -= movimento.quantidade

        if movimento.tipo_movimento == 'saida':
            produto.estoque += movimento.quantidade

        produto.save()

        return super(MovimentoEstoqueViewSet, self).destroy(request, *args, **kwargs)


class LocalViewSet(viewsets.ModelViewSet):

    serializer_class = LocalSerializer
    queryset = Local.objects.all()


class MedidaViewSet(viewsets.ModelViewSet):

    serializer_class = MedidaSerializer
    queryset = Medida.objects.all()


class DashBoardView(APIView):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        produtos = Produto.objects.count()
        sem_estoque = Produto.objects.filter(estoque__exact=0).count()
        maior_estoque = Produto.objects.order_by('-estoque')[0]
        categorias_produtos = {}

        categorias = CategoriaProduto.objects.all()

        # Cálculo da quantidade em estoque de produtos por categoria
        for categoria in categorias:
            produtosCategoria = Produto.objects.filter(subcategoria__categoria__id=categoria.id).aggregate(Sum('estoque'))

            if(produtosCategoria.get('estoque__sum')):
                categorias_produtos.update({categoria.nome: produtosCategoria.get('estoque__sum')})


        retorno = {
            "total_produtos": produtos,
            "sem_estoque": sem_estoque,
            "maior_estoque": '{} - {}' .format(maior_estoque.codigo, maior_estoque.descricao),
            "produtos_categorias": categorias_produtos
        }

        return Response(retorno)
