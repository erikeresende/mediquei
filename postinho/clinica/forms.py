from django import forms
from .models import Prontuario, Receita, Assinatura, Paciente, Medico, Medicamento, ItemReceita
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Digite sua senha', 
            'required': 'required',
            'autocomplete': 'current-password'
        })
    )

class CadastrarForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'crm', 'especialidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'crm': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ProntuarioForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        max_length=50000
    )

    class Meta:
        model = Prontuario
        fields = ['medico', 'paciente', 'data', 'descricao', 'assinatura_digital']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'assinatura_digital': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'dosagem', 'forma_farmaceutica', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite o nome do remédio', 'class': 'form-control'}),
            'dosagem': forms.TextInput(attrs={'placeholder': 'Digite a dosagem', 'class': 'form-control'}),
            'forma_farmaceutica': forms.TextInput(attrs={'placeholder': 'Digite a forma farmacêutica', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o medicamento aqui...', 'class': 'form-control'}),
        }

class ReceitaForm(forms.ModelForm):
    assinatura_digital = forms.CharField(widget=forms.HiddenInput(), required=False)  # Campo oculto para a assinatura

    class Meta:
        model = Receita
        fields = [ 'medicamento', 'dosagem', 'instrucoes', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medicamento': forms.Select(attrs={'class': 'form-control'}),  # Seleção do medicamento
            'dosagem': forms.TextInput(attrs={'class': 'form-control'}),
            'instrucoes': forms.TextInput(attrs={'class': 'form-control'})
        }

class ItemReceitaForm(forms.ModelForm):
    class Meta:
        model = ItemReceita
        fields = ['medicamento', 'dosagem']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),  # Seleção do medicamento
            'dosagem': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssinaturaForm(forms.ModelForm):
    class Meta:
        model = Assinatura
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
