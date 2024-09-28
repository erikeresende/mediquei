from django.shortcuts import render, redirect, get_object_or_404
from .models import Medico, Prontuario, Receita, Paciente, ItemReceita, Medicamento
from .forms import ProntuarioForm, ReceitaForm, PacienteForm, MedicoForm, MedicamentoForm, ItemReceitaForm, CadastrarForm
from django.forms import inlineformset_factory
import logging
import base64
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CadastrarForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View

def cadastrar(request):
    if request.method == 'POST':
        form = CadastrarForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário
            login(request, user)  # Loga o usuário após o registro
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')  # Redireciona para a página inicial
        else:
            # Se o formulário não for válido, adicione uma mensagem de erro
            messages.error(request, 'Erro ao criar conta. Verifique os dados e tente novamente.')
    else:
        form = CadastrarForm()  # Cria um novo formulário se o método não for POST

    return render(request, 'cadastrar.html', {'form': form})

class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login bem-sucedido!')
                return redirect('pagina_inicial')  # Redirecionar para a página inicial após login
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        elif 'next' in request.GET:
            messages.warning(request, 'Por favor, faça login para acessar essa página.')

        return render(request, 'login.html', {'form': form})

def logout_confirmar(request):
    if request.method == 'POST':
        logout(request)  # Realiza o logout
        messages.success(request, 'Você saiu com sucesso.')  # Mensagem de sucesso
        return redirect('login')  # Redireciona para a página de login após o logout

    # Se não for uma requisição POST, renderiza a página de confirmação
    return render(request, 'logout_confirmar.html') 



@login_required(login_url='login')  # Redireciona para o login se não estiver autenticado
def home_view(request):
    return render(request, 'pagina_inicial.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def pagina_inicial(request):
    context = {
        'username': request.user.username,  # Adiciona o nome do usuário ao contexto
    }
    return render(request, 'clinica/pagina_inicial.html', context)

@login_required
def base(request):
    context = {
        'username': request.user.username,  # Pass the username to the template
    }
    return render(request, 'clinica/base.html', context)

@login_required(login_url='login')
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'clinica/listar_pacientes.html', {'pacientes': pacientes})

@login_required(login_url='login')
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

@login_required(login_url='login')
def visualizar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    return render(request, 'clinica/visualizar_paciente.html', {'paciente': paciente})

@login_required(login_url='login')
def detalhe_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)  # Obtém o paciente ou retorna 404
    prontuarios = paciente.prontuarios.all()  # Obtém todos os prontuários associados ao paciente

    # Calcula a idade
    if paciente.data_nascimento:
        today = datetime.today()
        age = today.year - paciente.data_nascimento.year - ((today.month, today.day) < (paciente.data_nascimento.month, paciente.data_nascimento.day))
    else:
        age = None  # Ou algum valor padrão, se a data de nascimento não estiver definida

    return render(request, 'clinica/detalhe_paciente.html', {'paciente': paciente, 'prontuarios': prontuarios, 'age': age})

@login_required(login_url='login')
def adicionar_paciente(request):
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'clinica/adicionar_paciente.html', {'form': form})


@login_required(login_url='login')
def deletar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return render(request, 'clinica/deletar_paciente.html', {'paciente': paciente})

@login_required(login_url='login')
def criar_prontuario(request):
    medicamentos = Medicamento.objects.all()  # Obtém todos os medicamentos para o formulário

    if request.method == 'POST':
        form = ProntuarioForm(request.POST, request.FILES)

        if form.is_valid():
            prontuario = form.save(commit=False)
            assinatura_digital = request.POST.get('assinatura_digital')

            # Supondo que o paciente esteja sendo enviado no formulário
            paciente_id = request.POST.get('paciente_id')
            if paciente_id:
                try:
                    prontuario.paciente = Paciente.objects.get(id=paciente_id)
                except Paciente.DoesNotExist:
                    messages.error(request, "Paciente não encontrado.")
                    return render(request, 'clinica/criar_prontuario.html', {'form': form, 'medicamentos': medicamentos})

            # Processamento da assinatura digital
            if assinatura_digital:
                try:
                    header, encoded = assinatura_digital.split(',', 1)
                    formato = header.split(';')[0].split('/')[1]
                    if formato.lower() != 'png':
                        messages.error(request, "A assinatura deve ser em formato PNG.")
                        return render(request, 'clinica/criar_prontuario.html', {'form': form, 'medicamentos': medicamentos})

                    file_data = base64.b64decode(encoded)
                    image = Image.open(BytesIO(file_data))
                    png_image_io = BytesIO()
                    image.save(png_image_io, format='PNG')
                    file_name = f"assinatura.{formato}"
                    prontuario.assinatura_digital.save(file_name, ContentFile(png_image_io.getvalue()), save=False)
                except Exception as e:
                    logging.error(f'Erro ao processar a assinatura digital: {e}')
                    messages.error(request, "Ocorreu um erro ao processar a assinatura digital.")
                    return render(request, 'clinica/criar_prontuario.html', {'form': form, 'medicamentos': medicamentos})

            prontuario.save()

            # Processando medicamentos
            medicamentos_ids = request.POST.getlist('medicamentos[]')
            dosagens = request.POST.getlist('dosagens[]')
            formas = request.POST.getlist('formas[]')

            for i, medicamento_id in enumerate(medicamentos_ids):
                if medicamento_id:  # Verifica se o medicamento foi selecionado
                    medicamento = Medicamento.objects.get(id=medicamento_id)
                    dosagem = dosagens[i]
                    forma = formas[i]
                    # Criando uma receita para cada medicamento
                    Receita.objects.create(
                        medicamento=medicamento,
                        dosagem=dosagem,
                        prontuario=prontuario,
                        paciente=prontuario.paciente,
                        descricao=f'{forma}'  # Opcionalmente, você pode usar a forma como parte da descrição
                    )

            return redirect('pagina_inicial')
    else:
        form = ProntuarioForm()
    
    medicamentos = Medicamento.objects.all()
    return render(request, 'clinica/criar_prontuario.html', {
        'form': form,
        'medicamentos': medicamentos,
    })


@login_required(login_url='login')
def editar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, id=prontuario_id)
    if request.method == 'POST':
        form = ProntuarioForm(request.POST, instance=prontuario)
        if form.is_valid():
            prontuario = form.save(commit=False)
            form.save()
            return redirect('listar_prontuarios')
        else:
            logging.error(f'Form errors: {form.errors}')
    else:
        form = ProntuarioForm(instance=prontuario)
    return render(request, 'clinica/editar_prontuario.html', {'form': form, 'prontuario': prontuario})

@login_required(login_url='login')
def detalhes_prontuario(request, pk):
    prontuario = get_object_or_404(Prontuario, pk=pk)
    paciente = prontuario.paciente

    # Fetch all medications prescribed to the patient
    medicamentos = Receita.objects.filter(paciente=paciente).select_related('medicamento')

    context = {
        'prontuario': prontuario,
        'medicamentos': medicamentos,
    }
    return render(request, 'clinica/detalhes_prontuario.html', context)
    
@login_required(login_url='login')
def listar_receitas(request):
    receitas = Receita.objects.all()
    return render(request, 'clinica/listar_receitas.html', {'receitas': receitas})

@login_required(login_url='login')
def listar_prontuarios(request):
    search_query = request.GET.get('search')
    if search_query:
        prontuarios = Prontuario.objects.filter(paciente__nome__icontains=search_query)  # Ajuste conforme o campo que deseja pesquisar
    else:
        prontuarios = Prontuario.objects.all()  # Obtém todos os prontuários se não houver pesquisa

    return render(request, 'clinica/listar_prontuarios.html', {'prontuarios': prontuarios})

@login_required(login_url='login')
def deletar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, pk=prontuario_id)
    if request.method == 'POST':
        prontuario.delete()
        return redirect('listar_prontuarios')
    return render(request, 'clinica/deletar_prontuario_confirmar.html', {'prontuario': prontuario})

@login_required(login_url='login')
def adicionar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()  # Isso deve criar um novo médico sem especificar um id
            return redirect('listar_medicos')  # Redirecione para a lista de médicos
    else:
        form = MedicoForm()
    return render(request, 'clinica/adicionar_medico.html', {'form': form})

@login_required(login_url='login')
def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, pk=medico_id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('listar_medicos')  # Redireciona para a lista de médicos
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'clinica/editar_medico.html', {'form': form, 'medico': medico})

@login_required(login_url='login')
def deletar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)  # Obtém o médico ou retorna 404 se não encontrado

    if request.method == 'POST':
        medico.delete()  # Deleta o médico
        messages.success(request, 'Médico deletado com sucesso!')
        return redirect('listar_medicos')  # Redireciona para a lista de médicos
    return render(request, 'clinica/deletar_medico.html', {'medico': medico})  # Renderiza uma página de confirmação

@login_required(login_url='login')
def listar_medicos(request):
    medicos = Medico.objects.all()  # Obtém todos os médicos do banco de dados
    return render(request, 'clinica/listar_medicos.html', {'medicos': medicos})

@login_required(login_url='login')
def criar_receita(request):
    ItemReceitaFormSet = inlineformset_factory(Receita, ItemReceita, form=ItemReceitaForm, extra=1, can_delete=True)

    if request.method == 'POST':
        receita_form = ReceitaForm(request.POST, request.FILES)
        formset = ItemReceitaFormSet(request.POST, request.FILES)

        if receita_form.is_valid() and formset.is_valid():
            receita = receita_form.save(commit=False)

            assinatura_digital = request.POST.get('assinatura_digital')
            if assinatura_digital:
                try:
                    header, encoded = assinatura_digital.split(',', 1)
                    formato = header.split(';')[0].split('/')[1]
                    file_data = base64.b64decode(encoded)

                    if formato.lower() != 'png':
                        messages.error(request, "A assinatura deve ser em formato PNG.")
                        return render(request, 'clinica/criar_receita.html', {'form': receita_form, 'formset': formset})

                    image = Image.open(BytesIO(file_data))
                    png_image_io = BytesIO()
                    image.save(png_image_io, format='PNG')

                    file_name = f"assinatura_receita.png"
                    receita.assinatura_digital.save(file_name, ContentFile(png_image_io.getvalue()), save=False)
                except Exception as e:
                    logging.error(f'Erro ao processar a assinatura digital: {e}')
                    messages.error(request, "Ocorreu um erro ao processar a assinatura digital.")
                    return render(request, 'clinica/criar_receita.html', {'form': receita_form, 'formset': formset})

            receita.save()
            formset.instance = receita
            formset.save()
            messages.success(request, "Receita criada com sucesso!")
            return redirect('listar_receitas')
    else:
        receita_form = ReceitaForm()
        formset = ItemReceitaFormSet()

    return render(request, 'clinica/criar_receita.html', {'form': receita_form, 'formset': formset})

@login_required(login_url='login')
def deletar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    if request.method == 'POST':
        receita.delete()
        return redirect('listar_receitas')
    return render(request, 'clinica/deletar_receita_confirmar.html', {'receita': receita})

@login_required(login_url='login')
def adicionar_medicamento(request):
    if request.method == 'POST':
        medicamento_form = MedicamentoForm(request.POST)
        if medicamento_form.is_valid():
            medicamento_form.save()  # Salva o novo medicamento no banco de dados
            return redirect('listar_medicamentos')  # Redireciona para a lista de medicamentos após salvar
    else:
        medicamento_form = MedicamentoForm()

    return render(request, 'clinica/adicionar_medicamento.html', {'form': medicamento_form})

@login_required(login_url='login')
def editar_medicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)  # Obtém o medicamento ou retorna 404

    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)  # Preenche o formulário com os dados do medicamento existente
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            return redirect('listar_medicamentos')  # Redireciona para a lista de medicamentos após a edição
        else:
            logging.error(f'Erros no formulário de edição: {form.errors}')
    else:
        form = MedicamentoForm(instance=medicamento)  # Exibe o formulário preenchido com os dados atuais do medicamento

    return render(request, 'clinica/editar_medicamento.html', {'form': form, 'medicamento': medicamento})

@login_required(login_url='login')
def listar_medicamentos(request):
    medicamentos = Medicamento.objects.all()  # Obtém todos os medicamentos do banco de dados
    return render(request, 'clinica/listar_medicamentos.html', {'medicamentos': medicamentos})

@login_required(login_url='login')
def detalhe_medicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)  # Busca o medicamento ou retorna 404 se não encontrado
    return render(request, 'clinica/detalhe_medicamento.html', {'medicamento': medicamento})

@login_required(login_url='login')
def confirmar_deletar_medicamento(request, medicamento_id):
     # Aqui tentamos obter o objeto Medicamento
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    
    if request.method == 'POST':
        medicamento.delete()  # Realiza a exclusão do medicamento
        return redirect('listar_medicamentos')  # Redireciona para a lista de medicamentos

    return render(request, 'clinica/deletar_medicamento.html', {'medicamento': medicamento})

@login_required(login_url='login')
def deletar_medicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)  # Obtém o medicamento ou retorna 404

    if request.method == 'POST':
        medicamento.delete()  # Deleta o medicamento
        messages.success(request, 'Medicamento deletado com sucesso!')
        return redirect('listar_medicamentos')  # Redireciona para a lista de medicamentos
    return render(request, 'clinica/deletar_medicamento.html', {'medicamento': medicamento})  # Renderiza uma página de confirmação

@login_required(login_url='login')
def adicionar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a receita diretamente no banco de dados
            return redirect('listar_receitas')  # Redireciona para uma lista de receitas, por exemplo
    else:
        form = ReceitaForm()

    return render(request, 'clinica/adicionar_receita.html', {'form': form})

@login_required(login_url='login')
def listar_receitas(request):
    receitas = Receita.objects.all()  # Pega todas as receitas
    return render(request, 'clinica/listar_receitas.html', {'receitas': receitas})

@login_required(login_url='login')
def detalhes_receita(request, id):
    receita = get_object_or_404(Receita, id=id)
    return render(request, 'clinica/detalhes_receita.html', {'receita': receita})

@login_required(login_url='login')
def remover_receita(request, id):
    receita = get_object_or_404(Receita, id=id)
    
    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita removida com sucesso.')
        return redirect('listar_receitas')  # Redireciona para a página de listagem de receitas
    
    return render(request, 'clinica/confirmar_remocao_receita.html', {'receita': receita})

@login_required(login_url='login')
def editar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    paciente = receita.paciente  # Get the patient related to the prescription

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('listar_receitas')
    else:
        form = ReceitaForm(instance=receita)  # Only create the form with existing data if not POST

    context = {
        'form': form,
        'paciente': paciente,  # Pass the patient info to the template
        'receita_': receita.id,  # Add the receita ID to the context
    }
    return render(request, 'clinica/editar_receita.html', context)