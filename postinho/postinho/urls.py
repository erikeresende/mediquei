from django.contrib import admin
from django.urls import path, include
from clinica import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logout/confirmar/', views.logout_confirmar, name='logout_confirmar'), 

    # URLs para prontuários
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('prontuarios/', views.listar_prontuarios, name='listar_prontuarios'),
    path('prontuarios/<int:pk>/', views.detalhes_prontuario, name='detalhes_prontuario'),
    path('prontuarios/criar/', views.criar_prontuario, name='criar_prontuario'),
    path('prontuarios/<int:prontuario_id>/editar/', views.editar_prontuario, name='editar_prontuario'),
    path('prontuarios/<int:prontuario_id>/deletar/', views.deletar_prontuario, name='deletar_prontuario'),

    # URLs para receitas
    path('receitas/', views.listar_receitas, name='listar_receitas'),
    path('receitas/<int:id>/', views.detalhes_receita, name='detalhes_receita'),  # Verifique que o nome está correto aqui
    path('receitas/adicionar/', views.adicionar_receita, name='adicionar_receita'),
    path('receitas/<int:pk>/editar/', views.editar_receita, name='editar_receita'),
    path('receitas/criar/', views.criar_receita, name='criar_receita'),
    path('receitas/<int:receita_id>/remover/', views.remover_receita, name='remover_receita'),

    # URLs para pacientes
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/adicionar/', views.adicionar_paciente, name='adicionar_paciente'),
    path('pacientes/<int:id>/', views.visualizar_paciente, name='visualizar_paciente'),
    path('pacientes/<int:id>/editar/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/<int:id>/deletar/', views.deletar_paciente, name='deletar_paciente'),

    # URLs para médicos
    path('medicos/', views.listar_medicos, name='listar_medicos'),
    path('medicos/adicionar/', views.adicionar_medico, name='adicionar_medico'),
    path('medicos/<int:id>/editar/', views.editar_medico, name='editar_medico'),
    path('medicos/<int:id>/deletar/', views.deletar_medico, name='deletar_medico'),
    
    path('paciente/<int:paciente_id>/', views.detalhe_paciente, name='detalhe_paciente'),
    path('medicamentos/adicionar/', views.adicionar_medicamento, name='adicionar_medicamento'),
    path('medicamentos/', views.listar_medicamentos, name='listar_medicamentos'), 
    path('medicamentos/<int:medicamento_id>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamento/<int:medicamento_id>/deletar/confirmar/', views.deletar_medicamento, name='deletar_medicamento'),
    path('medicamento/<int:medicamento_id>/', views.detalhe_medicamento, name='detalhe_medicamento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
