# Generated by Django 5.1.1 on 2024-09-11 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0004_itemreceita'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='descricao',
            field=models.TextField(default='Nenhuma descrição disponível'),
        ),
    ]
