# Generated by Django 2.1.5 on 2019-02-04 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_auto_20190203_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentoestoque',
            name='tipo_movimento',
            field=models.CharField(choices=[('en', 'Entrada'), ('sd', 'Saída')], default='sd', max_length=2),
        ),
    ]
