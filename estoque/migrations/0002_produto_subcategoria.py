# Generated by Django 2.1.5 on 2019-02-03 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='subcategoria',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='estoque.SubCategoriaProduto'),
            preserve_default=False,
        ),
    ]
