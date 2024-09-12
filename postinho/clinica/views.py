from django.shortcuts import render, redirect, get_object_or_404
from .models import Medico, Prontuario, Receita, Paciente, ItemReceita, Medicamento
from .forms import ProntuarioForm, ReceitaForm, PacienteForm, MedicoForm, MedicamentoForm, ItemReceitaForm
from .utils import sign_data, verify_signature
from django.forms import formset_factory
import logging
import base64
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import processar_assinatura_digital 
from django.forms import inlineformset_factory

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
            logging.error(f'Form errors: {form.errors}')
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

from django.contrib import messages

def criar_prontuario(request):
    if request.method == 'POST':
        form = ProntuarioForm(request.POST, request.FILES)
        if form.is_valid():
            prontuario = form.save(commit=False)

            assinatura_digital = request.POST.get('assinatura_digital')
            if assinatura_digital:
                try:
                    # Processa a assinatura digital em base64
                    header, encoded = assinatura_digital.split(',', 1)
                    format = header.split(';')[0].split('/')[1]
                    file_data = base64.b64decode(encoded)

                    if format.lower() != 'png':
                        messages.error(request, "A assinatura deve ser em formato PNG.")
                        return render(request, 'clinica/criar_prontuario.html', {'form': form})

                    image = Image.open(BytesIO(file_data))
                    png_image_io = BytesIO()
                    image.save(png_image_io, format='PNG')

                    file_name = f"assinatura.{format}"
                    prontuario.assinatura_digital.save(file_name, ContentFile(png_image_io.getvalue()), save=False)
                except Exception as e:
                    logging.error(f'Erro ao processar a assinatura digital: {e}')
                    messages.error(request, "Ocorreu um erro ao processar a assinatura digital.")
                    return render(request, 'clinica/criar_prontuario.html', {'form': form})

            prontuario.save()
            return redirect('listar_prontuarios')
        else:
            logging.error(f'Form errors: {form.errors}')
            messages.error(request, "O formulário contém erros. Por favor, verifique.")
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
            logging.error(f'Form errors: {form.errors}')
    else:
        form = ProntuarioForm(instance=prontuario)
    return render(request, 'clinica/editar_prontuario.html', {'form': form, 'prontuario': prontuario})

def visualizar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, pk=prontuario_id)

    # A assinatura digital pode ser um arquivo ou uma string, ajuste conforme necessário.
    # Se você precisa verificar a assinatura digital, adicione a lógica aqui.

    return render(request, 'clinica/visualizar_prontuario.html', {'prontuario': prontuario})


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
    ItemReceitaFormSet = inlineformset_factory(Receita, ItemReceita, form=ItemReceitaForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        formset = ItemReceitaFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)

            # Processamento da assinatura digital
            assinatura_digital = request.POST.get('assinatura_digital')
            if assinatura_digital:
                try:
                    header, encoded = assinatura_digital.split(',', 1)
                    formato = header.split(';')[0].split('/')[1]
                    file_data = base64.b64decode(encoded)

                    if formato.lower() != 'png':
                        messages.error(request, "A assinatura deve ser em formato PNG.")
                        return render(request, 'clinica/criar_receita.html', {'form': form, 'formset': formset})

                    image = Image.open(BytesIO(file_data))
                    png_image_io = BytesIO()
                    image.save(png_image_io, format='PNG')

                    file_name = f"assinatura_receita.png"
                    receita.assinatura_digital.save(file_name, ContentFile(png_image_io.getvalue()), save=False)
                except Exception as e:
                    logging.error(f'Erro ao processar a assinatura digital: {e}')
                    messages.error(request, "Ocorreu um erro ao processar a assinatura digital.")
                    return render(request, 'clinica/criar_receita.html', {'form': form, 'formset': formset})

            receita.save()

            # Salvar os itens da receita
            formset.instance = receita
            formset.save()

            messages.success(request, "Receita criada com sucesso!")
            return redirect('listar_receitas')

        else:
            messages.error(request, "Erros no formulário ou nos itens da receita.")
            return render(request, 'clinica/criar_receita.html', {'form': form, 'formset': formset})

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
