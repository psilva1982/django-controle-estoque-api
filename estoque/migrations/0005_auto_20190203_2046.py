# Generated by Django 2.1.5 on 2019-02-03 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_auto_20190203_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentoestoque',
            name='data_hora',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
