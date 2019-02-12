from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models 
from django.db.models.signals import m2m_changed, post_save, pre_delete, \
    pre_save
from django.dispatch import receiver


class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=50, unique=True,
                            error_messages={'unique': "Já existe uma categoria cadastrada com este nome"})
    descricao = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome


class SubCategoriaProduto(models.Model):
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT)
    nome = models.CharField(max_length=50, null=False, blank=False,)
    descricao = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        unique_together = ('nome', 'categoria')

    def __str__(self):
        return self.categoria.nome + ' \ ' + self.nome


class Medida(models.Model):
    descricao = models.CharField(max_length=50, unique=True,
                           null=False, blank=False) 

    def __str__(self):
        return self.descricao


class Local(models.Model):
    descricao = models.CharField(max_length=50, unique=True,
                           null=False, blank=False)

    def __str__(self):
        return self.descricao


class Produto(models.Model):
    codigo = models.CharField(max_length=30, unique=True, null=False, blank=False,
                              error_messages={'unique': "Já existe um produto cadastrado com este código"})
    descricao = models.CharField(max_length=150, null=False, blank=False)
    subcategoria = models.ForeignKey(SubCategoriaProduto, on_delete=models.PROTECT)
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT)
    minimo = models.IntegerField(validators=[MinValueValidator(0)], default=5)
    estoque = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('descricao', 'subcategoria', 'local')

    def __str__(self): 
        return self.codigo + ' - ' + self.descricao


class MovimentoEstoque(models.Model):
    ENTRADA = 'entrada'
    SAIDA = 'saida'

    TIPO_MOVIMENTO = (
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    )

    data = models.DateField(auto_created=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    tipo_movimento = models.CharField(choices=TIPO_MOVIMENTO, default=SAIDA, max_length=7)
    motivo = models.CharField(max_length=150, null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    saldo_anterior = models.IntegerField(default=0, null=False, blank=False)
    observacao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def clean(self):
        if self.quantidade > self.produto.estoque and self.tipo_movimento == 'saida':
            raise ValidationError('Existe(m) apenas {} unidade(s) no estoque do produto {}' .format(
                self.produto.estoque, self.produto))

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Movimento do estoque'
        verbose_name_plural = 'Movimento do estoque'

