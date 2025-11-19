from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Equipamento, Categoria
from .forms import EquipamentoForm

# ==================== ABORDAGEM 1: FUNCTION-BASED VIEWS ====================

def lista_equipamentos(request):
    """
    View de Listagem - Exibe todos os equipamentos com busca e filtros
    """
    # Buscar todos os equipamentos
    equipamentos = Equipamento.objects.all().select_related('categoria')
    
    # Aplicar filtro de busca (nome ou serial)
    busca = request.GET.get('busca')
    if busca:
        equipamentos = equipamentos.filter(
            Q(nome__icontains=busca) | 
            Q(serial__icontains=busca)
        )
    
    # Aplicar filtro de categoria
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        equipamentos = equipamentos.filter(categoria_id=categoria_id)
    
    # Aplicar filtro de status
    status = request.GET.get('status')
    if status:
        equipamentos = equipamentos.filter(status=status)
    
    # Ordenar por data (mais recentes primeiro)
    equipamentos = equipamentos.order_by('-data')
    
    # Calcular estatísticas
    total_equipamentos = Equipamento.objects.count()
    em_uso = Equipamento.objects.filter(status='EM_USO').count()
    estoque = Equipamento.objects.filter(status='ESTOQUE').count()
    manutencao = Equipamento.objects.filter(status='MANUTENCAO').count()
    
    # Paginação (12 itens por página)
    paginator = Paginator(equipamentos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Buscar todas as categorias para o filtro
    categorias = Categoria.objects.all().order_by('nome')
    
    context = {
        'equipamentos': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categorias': categorias,
        'total_equipamentos': total_equipamentos,
        'em_uso': em_uso,
        'estoque': estoque,
        'manutencao': manutencao,
    }
    
    return render(request, 'lista_equipamentos.html', context)


def detalhe_equipamento(request, equipamento_id):
    """
    View de Detalhe - Exibe informações detalhadas de um equipamento específico
    """
    # Buscar o equipamento ou retornar 404 se não existir
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    
    # Buscar equipamentos relacionados (mesma categoria)
    equipamentos_relacionados = Equipamento.objects.filter(
        categoria=equipamento.categoria
    ).exclude(id=equipamento.id)[:4]
    
    context = {
        'equipamento': equipamento,
        'equipamentos_relacionados': equipamentos_relacionados,
    }
    
    return render(request, 'detalhe_equipamento.html', context)


def adicionar_equipamento(request):
    """
    View de Cadastro - Cria um novo equipamento
    Método GET: Exibe formulário vazio
    Método POST: Processa e salva os dados
    """
    if request.method == 'POST':
        # Processar dados enviados pelo formulário
        form = EquipamentoForm(request.POST)
        
        if form.is_valid():
            # Salvar no banco de dados
            equipamento = form.save()
            
            # Mensagem de sucesso
            messages.success(
                request, 
                f'Equipamento "{equipamento.nome}" cadastrado com sucesso!'
            )
            
            # Redirecionar para a lista
            return redirect('lista_equipamentos')
        else:
            # Se houver erros, a mensagem será exibida
            messages.error(
                request, 
                'Erro ao cadastrar equipamento. Verifique os campos.'
            )
    else:
        # Exibir formulário vazio (GET)
        form = EquipamentoForm()
    
    context = {
        'form': form,
        'titulo': 'Adicionar Equipamento',
        'icone': 'plus-circle',
    }
    
    return render(request, 'form_equipamento.html', context)


def editar_equipamento(request, equipamento_id):
    """
    View de Edição - Edita um equipamento existente
    """
    # Buscar o equipamento ou retornar 404
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    
    if request.method == 'POST':
        # Processar edição
        form = EquipamentoForm(request.POST, instance=equipamento)
        
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                f'Equipamento "{equipamento.nome}" atualizado com sucesso!'
            )
            return redirect('lista_equipamentos')
        else:
            messages.error(
                request, 
                'Erro ao atualizar equipamento. Verifique os campos.'
            )
    else:
        # Preencher formulário com dados existentes (GET)
        form = EquipamentoForm(instance=equipamento)
    
    context = {
        'form': form,
        'equipamento': equipamento,
        'titulo': 'Editar Equipamento',
        'icone': 'pencil-square',
    }
    
    return render(request, 'form_equipamento.html', context)


def excluir_equipamento(request, equipamento_id):
    """
    View de Exclusão - Remove um equipamento
    """
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    
    if request.method == 'POST':
        nome = equipamento.nome
        equipamento.delete()
        messages.success(request, f'Equipamento "{nome}" excluído com sucesso!')
        return redirect('lista_equipamentos')
    
    context = {
        'equipamento': equipamento,
    }
    
    return render(request, 'confirmar_exclusao.html', context)


# ==================== ABORDAGEM 2: CLASS-BASED VIEWS ====================
# (Comentadas - descomente se preferir usar classes)

"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class EquipamentoListView(ListView):
    model = Equipamento
    template_name = 'lista_equipamentos.html'
    context_object_name = 'equipamentos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria')
        
        # Filtros
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(serial__icontains=busca)
            )
        
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-data')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['total_equipamentos'] = Equipamento.objects.count()
        context['em_uso'] = Equipamento.objects.filter(status='EM_USO').count()
        context['estoque'] = Equipamento.objects.filter(status='ESTOQUE').count()
        context['manutencao'] = Equipamento.objects.filter(status='MANUTENCAO').count()
        return context


class EquipamentoDetailView(DetailView):
    model = Equipamento
    template_name = 'detalhe_equipamento.html'
    context_object_name = 'equipamento'
    pk_url_kwarg = 'equipamento_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipamentos_relacionados'] = Equipamento.objects.filter(
            categoria=self.object.categoria
        ).exclude(id=self.object.id)[:4]
        return context


class EquipamentoCreateView(CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'form_equipamento.html'
    success_url = reverse_lazy('lista_equipamentos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Adicionar Equipamento'
        context['icone'] = 'plus-circle'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipamento cadastrado com sucesso!')
        return super().form_valid(form)


class EquipamentoUpdateView(UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'form_equipamento.html'
    success_url = reverse_lazy('lista_equipamentos')
    pk_url_kwarg = 'equipamento_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Equipamento'
        context['icone'] = 'pencil-square'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipamento atualizado com sucesso!')
        return super().form_valid(form)


class EquipamentoDeleteView(DeleteView):
    model = Equipamento
    template_name = 'confirmar_exclusao.html'
    success_url = reverse_lazy('lista_equipamentos')
    pk_url_kwarg = 'equipamento_id'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Equipamento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)
"""