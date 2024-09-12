from django.db import models
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import base64

# Funções de validação
def validate_crm(value):
    if not re.match(r'^\d{4,6}-\d{1,2}$', value):
        raise ValidationError('O CRM deve estar no formato correto.')

def validate_data_nascimento(value):
    if value > date.today():
        raise ValidationError('A data de nascimento não pode ser uma data futura.')

def validate_file_extension(value):
    if not value.name.lower().endswith('.png'):
        raise ValidationError('A assinatura deve estar em formato PNG.')

# Modelos
class Medico(models.Model):
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, validators=[validate_crm])

    def __str__(self):
        return f"{self.nome} (CRM: {self.crm})"

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField(validators=[validate_data_nascimento])

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

class Medicamento(models.Model):
    medicamento = models.CharField(max_length=255, default='Sem Medicamento')
    dosagem = models.CharField(max_length=255, default='Sem dosagem')

    def __str__(self):
        return self.medicamento

class Receita(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateField()
    descricao = models.TextField(default='Nenhuma descrição disponível')
    assinatura_digital = models.ImageField(upload_to='assinaturas/', blank=True, null=True, validators=[validate_file_extension])

    def clean(self):
        if not self.descricao:
            raise ValidationError('A descrição não pode estar vazia.')

    def __str__(self):
        return f'Receita para {self.paciente.nome} em {self.data}'

    class Meta:
        ordering = ['-data']
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'

class ItemReceita(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='itens')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosagem = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.medicamento.medicamento} - {self.dosagem}'

class Prontuario(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateField()
    descricao = models.TextField()
    assinatura_digital = models.ImageField(upload_to='assinaturas/', blank=True, null=True, validators=[validate_file_extension])

    def clean(self):
        if not self.descricao:
            raise ValidationError('A descrição não pode estar vazia.')

    def __str__(self):
        return f'Prontuário de {self.paciente.nome} em {self.data}'

class Assinatura(models.Model):
    arquivo = models.ImageField(upload_to='assinaturas/', validators=[validate_file_extension])
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='assinaturas', null=True, blank=True)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='assinaturas', null=True, blank=True)

    def __str__(self):
        return f'Assinatura para {self.prontuario if self.prontuario else self.receita}'
