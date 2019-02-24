from django.db.models import F
from django_filters import rest_framework as filters

from estoque.models import Produto


class ProdutoFilter(filters.FilterSet):
    status = filters.CharFilter(method='status_filter')

    class Meta:
        model = Produto
        fields = ['local', 'subcategoria', 'medida', 'status']

    def status_filter(self, queryset, name, value):
        if value == 'normal':
            queryset = queryset.filter(estoque__gt=F('minimo'))
        
        elif value == 'baixo':
            queryset = queryset.filter(estoque__gt=0).filter(estoque__lte=F('minimo'))

        elif value == 'sem':
            queryset = queryset.filter(estoque=0)

        return queryset


