from django.views.generic import View
from django.db.models import F
from django.utils import timezone
from estoque.models import *
from estoque.api.render import PdfRender


class RelatorioProdutos(View):

   def get(self, request):

      estoque = request.GET.get('estoque' or None)
      local = request.GET.get('local' or None)
      subcategoria = request.GET.get('subcategoria' or None)
      medida = request.GET.get('medida' or None)
      descricao = request.GET.get('descricao' or None)

      produtos = Produto.objects.all()

      if estoque == 'sem':
         produtos = produtos.filter(estoque=0)

      elif estoque == 'baixo':
         produtos = produtos.filter(estoque__gt=0).filter(estoque__lte=F('minimo'))

      elif estoque == 'normal':
         produtos = produtos.filter(estoque__gt=F('minimo'))

      if local:
         produtos = produtos.filter(local=local)

      if subcategoria:
         produtos = produtos.filter(subcategoria=subcategoria)

      if medida:
         produtos = produtos.filter(medida=medida)

      if descricao:
         produtos = produtos.filter(codigo__icontains=descricao) | produtos.filter(descricao__icontains=descricao)

      produtos = produtos.order_by('subcategoria__categoria__nome', 'subcategoria__nome', 'descricao')

      hoje = timezone.now()
      params = {
         'hoje': hoje,
         'produtos': produtos,
         'request': request
      }

      return PdfRender.render('relatorios/produtos.html', params)
