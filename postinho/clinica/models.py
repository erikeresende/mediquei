from django.db import models
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Corrigido o nome do campo
    email = models.EmailField(max_length=254, blank=True, null=True)  # Usando EmailField para o email

    def __str__(self):
        return self.user.username  # Retorna o nome de usuário associado

# Criar um perfil de usuário automaticamente quando um novo usuário é criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Salvar o perfil do usuário sempre que o usuário for salvo
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Medico(models.Model):
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, validators=[validate_crm], unique=True)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} (CRM: {self.crm})"

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    @property
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year
        if today.month < self.data_nascimento.month or (today.month == self.data_nascimento.month and today.day < self.data_nascimento.day):
            age -= 1
        return age

    def __str__(self):
        return self.nome

class Prontuario(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, related_name='prontuarios', on_delete=models.CASCADE)
    data = models.DateTimeField(default=date.today)
    descricao = models.TextField(blank=False)

    assinatura_digital = models.ImageField(upload_to='assinaturas/', blank=True, null=True, validators=[validate_file_extension])
    receitas = models.ManyToManyField('Receita', related_name='prontuarios', blank=True)

    def clean(self):
        if not self.descricao:
            raise ValidationError('A descrição não pode estar vazia.')

    def __str__(self):
        return f'Prontuário de {self.paciente.nome} em {self.data}'

class Medicamento(models.Model):
    nome = models.CharField(max_length=255, default='')
    dosagem = models.CharField(max_length=50)
    forma_farmaceutica = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nome

class Receita(models.Model):
    prontuario = models.ForeignKey(Prontuario, related_name='receitas_list', on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateTimeField(default=date.today)
    descricao = models.TextField(default='Nenhuma descrição disponível', blank=False)
    assinatura_digital = models.ImageField(upload_to='assinaturas/', blank=True, null=True, validators=[validate_file_extension])
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosagem = models.CharField(max_length=50)
    instrucoes = models.TextField(blank=True, null=True)
    medicamentos_prescritos = models.ManyToManyField(Medicamento, related_name='receitas')  # Example

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
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='itens_receita')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='itens_receita')
    dosagem = models.CharField(max_length=255, blank=False)
    forma_farmaceutica = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.medicamento.nome} - {self.dosagem} - {self.forma_farmaceutica}'

class Assinatura(models.Model):
    arquivo = models.ImageField(upload_to='assinaturas/', validators=[validate_file_extension])
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='assinaturas', null=True, blank=True)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='assinaturas', null=True, blank=True)

    def clean(self):
        if not self.prontuario and not self.receita:
            raise ValidationError('Deve estar associado a um prontuário ou receita.')

    def __str__(self):
        return f'Assinatura para {self.prontuario.paciente.nome if self.prontuario else self.receita.paciente.nome}'
