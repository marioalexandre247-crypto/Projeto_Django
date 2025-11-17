from django import forms
from .models import Equipamento, Categoria

class EquipamentoForm(forms.ModelForm):
    """
    ModelForm para criar e editar Equipamentos
    """
    
    class Meta:
        model = Equipamento
        fields = ['nome', 'serial', 'data', 'categoria', 'status']
        
        # Widgets personalizados para melhor UX
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do equipamento',
                'required': True,
            }),
            'serial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o número de série',
                'required': True,
            }),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'status': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
        }
        
        # Labels personalizados
        labels = {
            'nome': 'Nome do Equipamento',
            'serial': 'Número de Série',
            'data': 'Data de Aquisição',
            'categoria': 'Categoria',
            'status': 'Status',
        }
        
        # Mensagens de erro personalizadas
        error_messages = {
            'nome': {
                'required': 'O nome do equipamento é obrigatório.',
                'max_length': 'O nome não pode ter mais de 200 caracteres.',
            },
            'serial': {
                'required': 'O número de série é obrigatório.',
                'unique': 'Já existe um equipamento com este número de série.',
                'max_length': 'O número de série não pode ter mais de 100 caracteres.',
            },
            'data': {
                'required': 'A data de aquisição é obrigatória.',
                'invalid': 'Data inválida. Use o formato dd/mm/aaaa.',
            },
            'categoria': {
                'required': 'Selecione uma categoria.',
            },
            'status': {
                'required': 'Selecione o status do equipamento.',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classe 'required' aos campos obrigatórios
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
        
        # Ordenar categorias alfabeticamente
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nome')
    
    def clean_serial(self):
        """
        Validação customizada para o número de série
        """
        serial = self.cleaned_data.get('serial')
        
        # Converter para maiúsculas
        serial = serial.upper().strip()
        
        # Verificar se já existe (exceto para edição)
        equipamento_existente = Equipamento.objects.filter(serial=serial)
        if self.instance.pk:
            equipamento_existente = equipamento_existente.exclude(pk=self.instance.pk)
        
        if equipamento_existente.exists():
            raise forms.ValidationError(
                'Já existe um equipamento com este número de série.'
            )
        
        return serial
    
    def clean_nome(self):
        """
        Validação customizada para o nome
        """
        nome = self.cleaned_data.get('nome')
        
        # Capitalizar primeira letra de cada palavra
        nome = nome.strip().title()
        
        return nome
    
    def clean_data(self):
        """
        Validação customizada para a data
        """
        from datetime import date
        data = self.cleaned_data.get('data')
        
        # Verificar se a data não é futura
        if data and data > date.today():
            raise forms.ValidationError(
                'A data de aquisição não pode ser no futuro.'
            )
        
        return data