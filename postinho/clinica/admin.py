from django.contrib import admin
from .models import Medico, Paciente, Prontuario, Receita, Assinatura, ItemReceita

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento')

@admin.register(Prontuario)
class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'data', 'descricao')

class ItemReceitaInline(admin.TabularInline):
    model = ItemReceita
    extra = 1

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'data', 'mostrar_medicamentos')
    inlines = [ItemReceitaInline]

    def mostrar_medicamentos(self, obj):
        return ", ".join([f"{item.medicamento} ({item.dosagem})" for item in obj.itens.all()])
    mostrar_medicamentos.short_description = 'Medicamentos'

@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ('prontuario', 'arquivo')
