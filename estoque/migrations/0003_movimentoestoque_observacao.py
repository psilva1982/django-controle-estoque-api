# Generated by Django 2.1.5 on 2019-02-03 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_produto_subcategoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentoestoque',
            name='observacao',
            field=models.TextField(blank=True, null=True),
        ),
    ]
