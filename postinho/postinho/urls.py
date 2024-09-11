from django.contrib import admin
from django.urls import path
from clinica import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs para prontuários
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('prontuarios/', views.listar_prontuarios, name='listar_prontuarios'),
    path('prontuarios/<int:prontuario_id>/editar/', views.editar_prontuario, name='editar_prontuario'),
    path('prontuarios/criar/', views.criar_prontuario, name='criar_prontuario'),
    path('prontuarios/<int:prontuario_id>/', views.visualizar_prontuario, name='visualizar_prontuario'),
    path('prontuarios/<int:prontuario_id>/deletar/', views.deletar_prontuario, name='deletar_prontuario'),
    
    # URLs para receitas
    path('receitas/', views.listar_receitas, name='listar_receitas'),
    path('receitas/criar/', views.criar_receita, name='criar_receita'),
    path('receitas/<int:receita_id>/deletar/', views.deletar_receita, name='deletar_receita'),

    # URLs para pacientes
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/adicionar/', views.adicionar_paciente, name='adicionar_paciente'),
    path('pacientes/<int:id>/', views.visualizar_paciente, name='visualizar_paciente'),
    path('pacientes/<int:id>/editar/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/<int:id>/deletar/', views.deletar_paciente, name='deletar_paciente'),

    # URLs para pacientes
    path('medico/adicionar/', views.criar_medico, name='criar_medico'),
    path('receita/criar/', views.criar_receita, name='criar_receita'),  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
