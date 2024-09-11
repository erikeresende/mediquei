from django.shortcuts import render, redirect, get_object_or_404
from .models import Medico, Prontuario, Receita, Paciente, ItemReceita, Medicamento
from .forms import ProntuarioForm, ReceitaForm, PacienteForm, MedicoForm, MedicamentoForm, ItemReceitaForm
from .utils import sign_data, verify_signature
from django.forms import formset_factory
import logging

def pagina_inicial(request):
    return render(request, 'clinica/pagina_inicial.html')

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'clinica/listar_pacientes.html', {'pacientes': pacientes})

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'clinica/editar_paciente.html', {'form': form, 'paciente': paciente})

def visualizar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    return render(request, 'clinica/visualizar_paciente.html', {'paciente': paciente})

def adicionar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'clinica/adicionar_paciente.html', {'form': form})

def deletar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return render(request, 'clinica/deletar_paciente.html', {'paciente': paciente})

def criar_prontuario(request):
    if request.method == 'POST':
        form = ProntuarioForm(request.POST)
        if form.is_valid():
            prontuario = form.save(commit=False)
            assinatura_digital = request.POST.get('assinatura_digital')
            if assinatura_digital:
                prontuario.assinatura_digital = assinatura_digital
            prontuario.save()
            return redirect('listar_prontuarios')
    else:
        form = ProntuarioForm()
    return render(request, 'clinica/criar_prontuario.html', {'form': form})

def editar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, id=prontuario_id)
    if request.method == 'POST':
        form = ProntuarioForm(request.POST, instance=prontuario)
        if form.is_valid():
            form.save()
            return redirect('listar_prontuarios')
    else:
        form = ProntuarioForm(instance=prontuario)
    return render(request, 'clinica/editar_prontuario.html', {'form': form, 'prontuario': prontuario})

def visualizar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, pk=prontuario_id)
    data_bytes = prontuario.descricao.encode()
    is_valid = verify_signature(data_bytes, prontuario.assinatura_digital, "public_key.pem")
    return render(request, 'clinica/visualizar_prontuario.html', {'prontuario': prontuario, 'is_valid': is_valid})

def listar_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'clinica/listar_receitas.html', {'receitas': receitas})

def listar_prontuarios(request):
    prontuarios = Prontuario.objects.all()
    return render(request, 'clinica/listar_prontuarios.html', {'prontuarios': prontuarios})

def deletar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, pk=prontuario_id)
    if request.method == 'POST':
        prontuario.delete()
        return redirect('listar_prontuarios')
    return render(request, 'clinica/deletar_prontuario_confirmar.html', {'prontuario': prontuario})

def criar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_medicos')
    else:
        form = MedicoForm()
    return render(request, 'clinica/criar_medico.html', {'form': form})

def criar_receita(request):
    ItemReceitaFormSet = formset_factory(ItemReceitaForm, extra=1)

    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        formset = ItemReceitaFormSet(request.POST)
        assinatura_digital = request.POST.get('assinatura_digital')

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)
            
            if assinatura_digital:
                receita.assinatura_digital = assinatura_digital
            receita.save()

            for item_form in formset:
                if item_form.cleaned_data:  # Verifica se há dados limpos para salvar
                    medicamento = item_form.cleaned_data.get('medicamento')
                    dosagem = item_form.cleaned_data.get('dosagem')
                    if medicamento and dosagem:
                        ItemReceita.objects.create(
                            receita=receita,
                            medicamento=medicamento,
                            dosagem=dosagem
                        )

            return redirect('listar_receitas')
        else:
            logging.error(f'Form errors: {form.errors}')
            logging.error(f'Formset errors: {formset.errors}')

    else:
        form = ReceitaForm()
        formset = ItemReceitaFormSet()

    return render(request, 'clinica/criar_receita.html', {'form': form, 'formset': formset})

def deletar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    if request.method == 'POST':
        receita.delete()
        return redirect('listar_receitas')
    return render(request, 'clinica/deletar_receita_confirmar.html', {'receita': receita})
