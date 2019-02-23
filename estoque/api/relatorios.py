from django.views.generic import View
from django.utils import timezone
from estoque.models import *
from estoque.api.render import PdfRender

class RelatorioProdutos(View):

   def get(self, request):
      produtos = Produto.objects.all()
      hoje = timezone.now()
      params = {
         'hoje': hoje,
         'produtos': produtos,
         'request': request
      }
      return PdfRender.render('relatorios/produtos.html', params)
