# Generated by Django 2.1.5 on 2019-02-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0022_auto_20190206_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentoestoque',
            name='tipo_movimento',
            field=models.CharField(choices=[('entrada', 'Entrada'), ('saída', 'Saída')], default='saída', max_length=7),
        ),
    ]
