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
         estoque = 'Sem estoque'

      elif estoque == 'baixo':
         produtos = produtos.filter(estoque__gt=0).filter(estoque__lte=F('minimo'))
         estoque = 'Estoque baixo'

      elif estoque == 'normal':
         produtos = produtos.filter(estoque__gt=F('minimo'))
         estoque = 'Normal'

      if local:
         produtos = produtos.filter(local=local)
         local = Local.objects.get(pk=local).descricao

      if subcategoria:
         produtos = produtos.filter(subcategoria=subcategoria)
         subcategoria = SubCategoriaProduto.objects.get(pk=subcategoria)

      if medida:
         produtos = produtos.filter(medida=medida)
         medida = Medida.objects.get(pk=medida).descricao

      if descricao:
         produtos = produtos.filter(codigo__icontains=descricao) | produtos.filter(descricao__icontains=descricao)

      produtos = produtos.order_by('subcategoria__categoria__nome', 'subcategoria__nome', 'descricao')

      hoje = timezone.now()

      descricao = self.verifica_parametro(descricao, 'Não informado')
      medida = self.verifica_parametro(medida, 'Todas')
      subcategoria = self.verifica_parametro(subcategoria, 'Todas')
      local = self.verifica_parametro(local, 'Todos')
      estoque = self.verifica_parametro(estoque, 'Todos')

      params = {
         'hoje': hoje,
         'produtos': produtos,
         'request': request,
         'estoque': estoque,
         'local': local,
         'subcategoria': subcategoria,
         'medida': medida,
         'descricao': descricao
      }

      return PdfRender.render('relatorios/produtos.html', params)

   def verifica_parametro(self, parametro, recebe):

      if parametro == None:
         parametro = recebe

      return parametro
