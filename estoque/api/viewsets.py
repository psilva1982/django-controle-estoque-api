from django.db.models import Q
from django.db.models import Sum

import datetime

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from estoque.models import CategoriaProduto
from estoque.models import Local
from estoque.models import Medida
from estoque.models import MovimentoEstoque
from estoque.models import Produto
from estoque.models import SubCategoriaProduto

from estoque.api.serializers import LocalSerializer
from estoque.api.serializers import MedidaSerializer
from estoque.api.serializers import MovimentoEstoqueSerializer
from estoque.api.serializers import ProdutoSerializer
from estoque.api.serializers import SubCategoriaProdutoSerializer
from estoque.api.serializers import CategoriaProdutoSerializer


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

    #authentication_classes = (JWTAuthentication, )
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        # Total de produtos cadastrados
        total_produtos = Produto.objects.count()

        # Total de produtos sem estoque
        sem_estoque = Produto.objects.filter(estoque__exact=0).count()

        # Produto com maior estoque
        maior_estoque = Produto.objects.order_by('-estoque')[0]

        # Maior saida
        maior_saida_qtde = 0
        maior_saida_produto = ''

        # Entrada / Saída mensal
        entrada_mensal = 0
        saida_mensal = 0

        # Gráfico de pizza
        categorias_produtos = {}
        categorias = CategoriaProduto.objects.all()

        # Gráfico de barras
        entradas = []
        saidas = []

        # Gráfico de Pizza - Cálculo da quantidade em estoque de produtos por categoria
        for categoria in categorias:
            produtosCategoria = Produto.objects.filter(subcategoria__categoria__id=categoria.id).aggregate(Sum('estoque'))

            if produtosCategoria.get('estoque__sum'):
                categorias_produtos.update({categoria.nome: produtosCategoria.get('estoque__sum')})

        ano = int(datetime.datetime.now().strftime('%Y'))
        mes_atual = int(datetime.datetime.now().strftime('%m'))

        # Gráfico de barras - Cálculo dos movimentos por mes
        for mes in range(1, 13):
            inicio = datetime.date(ano, mes, 1)
            fim: datetime.date

            try:
                if mes == 2:
                    fim = datetime.date(ano, mes, 29)
                else:
                    fim = datetime.date(ano, mes, 31)

            except:

                if mes == 2:
                    fim = datetime.date(ano, mes, 28)
                else:
                    fim = datetime.date(ano, mes, 30)

            entrada = MovimentoEstoque.objects.filter(tipo_movimento__exact='entrada')\
                .filter(data__range=(inicio, fim)).count()

            saida = MovimentoEstoque.objects.filter(tipo_movimento__exact='saida')\
                .filter(data__range=(inicio, fim)).count()

            if mes == mes_atual:
                entrada_mensal = entrada
                saida_mensal = saida


                produtos = Produto.objects.all()
                for produto in produtos:

                    total_saida = MovimentoEstoque.objects.filter(produto_id=produto.id) \
                       .filter(data__range=(inicio, fim)) \
                       .filter(tipo_movimento='saida') \
                       .aggregate(Sum('quantidade'))

                    total = total_saida.get('quantidade__sum')

                    if (total is not None) and (total > maior_saida_qtde):
                        maior_saida_qtde = total
                        maior_saida_produto = produto.codigo + ' - ' + produto.descricao

            entradas.append(entrada)
            saidas.append(saida)

        retorno = {
            "total_produtos": total_produtos,
            "sem_estoque": sem_estoque,
            "maior_estoque_produto": '{} - {}' .format(maior_estoque.codigo, maior_estoque.descricao),
            "maior_estoque_qtde": maior_estoque.estoque,
            "maior_saida_produto": maior_saida_produto,
            "maior_saida_qtde": maior_saida_qtde,
            "produtos_categorias": categorias_produtos,
            "ano": ano,
            "entrada_mensal": entrada_mensal,
            "saida_mensal": saida_mensal,
            "entradas": entradas,
            "saidas": saidas
        }

        return Response(retorno)


