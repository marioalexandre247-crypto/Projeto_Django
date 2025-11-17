from django.urls import path
from . import views

urlpatterns = [
    # Lista de equipamentos (página inicial)
    path('', views.lista_equipamentos, name='lista_equipamentos'),
    
    # Detalhe de um equipamento específico
    path('equipamento/<int:equipamento_id>/', views.detalhe_equipamento, name='detalhe_equipamento'),
    
    # Adicionar novo equipamento
    path('adicionar/', views.adicionar_equipamento, name='adicionar_equipamento'),
    
    # Editar equipamento existente
    path('editar/<int:equipamento_id>/', views.editar_equipamento, name='editar_equipamento'),
    
    # Excluir equipamento
    path('excluir/<int:equipamento_id>/', views.excluir_equipamento, name='excluir_equipamento'),
]


# ==================== ALTERNATIVA COM CLASS-BASED VIEWS ====================
# (Descomente se quiser usar CBVs ao invés de FBVs)

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EquipamentoListView.as_view(), name='lista_equipamentos'),
    path('equipamento/<int:equipamento_id>/', views.EquipamentoDetailView.as_view(), name='detalhe_equipamento'),
    path('adicionar/', views.EquipamentoCreateView.as_view(), name='adicionar_equipamento'),
    path('editar/<int:equipamento_id>/', views.EquipamentoUpdateView.as_view(), name='editar_equipamento'),
    path('excluir/<int:equipamento_id>/', views.EquipamentoDeleteView.as_view(), name='excluir_equipamento'),
]
"""