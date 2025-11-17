# Seu_App/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 1. URL de Listagem
    path('', views.listar_equipamentos, name='lista_equipamentos'),
    
    # 2. URL de Detalhe (recebe o pk/ID como inteiro)
    path('<int:pk>/', views.detalhe_equipamento, name='detalhe_equipamento'),
    
    # 3. URL de Cadastro (chama a view baseada em classe)
    path('novo/', views.EquipamentoCreateView.as_view(), name='cadastro_equipamento'),
]