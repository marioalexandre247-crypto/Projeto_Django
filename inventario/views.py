from django.shortcuts import render

# Create your views here.
# Seu_App/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipamento
from .forms import EquipamentoForm
from django.views import View # Usaremos views baseadas em classe para o cadastro

# 1. View de Listagem (Função Simples)
def listar_equipamentos(request):
    """
    Busca todos os equipamentos no banco e os envia para o template de listagem.
    """
    equipamentos = Equipamento.objects.all()
    contexto = {
        'equipamentos': equipamentos
    }
    return render(request, 'equipamentos/lista_equipamentos.html', contexto)

# 2. View de Detalhe (Função Simples)
def detalhe_equipamento(request, pk):
    """
    Recebe um ID (pk), busca um equipamento específico e envia para o template de detalhe.
    Se não encontrar, retorna um 404.
    """
    equipamento = get_object_or_404(Equipamento, pk=pk)
    contexto = {
        'equipamento': equipamento
    }
    return render(request, 'equipamentos/detalhe_equipamento.html', contexto)

# 3. View de Cadastro (View Baseada em Classe)
class EquipamentoCreateView(View):
    """
    Lida com a exibição e submissão do formulário de cadastro de equipamento.
    """
    def get(self, request):
        """
        Método GET: Exibe o formulário vazio.
        """
        form = EquipamentoForm()
        contexto = {
            'form': form
        }
        return render(request, 'equipamentos/cadastro_equipamento.html', contexto)

    def post(self, request):
        """
        Método POST: Processa os dados do formulário.
        """
        form = EquipamentoForm(request.POST)

        if form.is_valid():
            # Salva o novo objeto no banco de dados
            form.save()
            
            # Redireciona o usuário para a lista de equipamentos após o sucesso
            return redirect('lista_equipamentos') # Assumindo o nome da URL é 'lista_equipamentos'
        
        # Se o formulário for inválido, re-exibe a página com os erros
        contexto = {
            'form': form
        }
        return render(request, 'equipamentos/cadastro_equipamento.html', contexto)