# Generated by Django 5.1.1 on 2024-09-12 17:32

import clinica.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0011_alter_medico_options_alter_paciente_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medico',
            options={},
        ),
        migrations.AddField(
            model_name='assinatura',
            name='receita',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assinaturas', to='clinica.receita'),
        ),
        migrations.AlterField(
            model_name='assinatura',
            name='arquivo',
            field=models.ImageField(upload_to='assinaturas/', validators=[clinica.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='assinatura',
            name='prontuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assinaturas', to='clinica.prontuario'),
        ),
        migrations.AlterField(
            model_name='medico',
            name='crm',
            field=models.CharField(max_length=20, validators=[clinica.models.validate_crm]),
        ),
        migrations.AlterField(
            model_name='prontuario',
            name='medico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinica.medico'),
        ),
        migrations.AlterField(
            model_name='receita',
            name='assinatura_digital',
            field=models.ImageField(blank=True, null=True, upload_to='assinaturas/', validators=[clinica.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='receita',
            name='medico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinica.medico'),
        ),
    ]
