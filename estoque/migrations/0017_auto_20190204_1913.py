# Generated by Django 2.1.5 on 2019-02-04 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0016_auto_20190204_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategoriaproduto',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='estoque.CategoriaProduto'),
        ),
    ]
