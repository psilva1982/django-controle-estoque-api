"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from seguranca.token import TokenView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from estoque.api.viewsets import CategoriaViewSet
from estoque.api.viewsets import SubCategoriaViewSet
from estoque.api.viewsets import ProdutoViewSet
from estoque.api.viewsets import MovimentoEstoqueViewSet
from estoque.api.viewsets import LocalViewSet
from estoque.api.viewsets import MedidaViewSet
from estoque.api.viewsets import DashBoardView

from estoque.api.relatorios import RelatorioProdutos

router = routers.DefaultRouter()
router.register(r'categorias',  CategoriaViewSet) 
router.register(r'subcategorias', SubCategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'movimentos', MovimentoEstoqueViewSet)
router.register(r'locais', LocalViewSet)
router.register(r'medidas', MedidaViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(r'dashboard', DashBoardView.as_view()),
    path(r'relatorios/produtos/', RelatorioProdutos.as_view()),

    path('api/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('admin/', admin.site.urls),
]

admin.site.site_header = 'Gestão de Estoque'
admin.site.index_title = 'Administração'
admin.site.site_title = 'Seja bem vindo'
admin.site.site_url = 'http://localhost:4200/'
