from django import forms
from .models import Prontuario, Receita, Assinatura, Paciente, Medico, Medicamento, ItemReceita

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'crm']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'crm': forms.TextInput(attrs={'class': 'form-control'}),
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
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'assinatura_digital': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['medicamento', 'dosagem']
        widgets = {
            'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosagem': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReceitaForm(forms.ModelForm):
    assinatura_digital = forms.CharField(widget=forms.HiddenInput(), required=False)  # Campo oculto para a assinatura

    class Meta:
        model = Receita
        fields = ['medico', 'paciente', 'data', 'descricao', 'assinatura_digital']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'assinatura_digital': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ItemReceitaForm(forms.ModelForm):
    class Meta:
        model = ItemReceita
        fields = ['medicamento', 'dosagem']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),  # Alterado para Select se Medicamento for um ForeignKey
            'dosagem': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssinaturaForm(forms.ModelForm):
    class Meta:
        model = Assinatura
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
