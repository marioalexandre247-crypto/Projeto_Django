from django.db import models

# Create your models here.


#maxlength para limite de letras
#unique garante que não terá categorias com nomes duplicados
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class meta:
        meta_name = 'Categoria'
        meta_name_plutal = 'Categorias'
    
    def __str__(self):
        return self.nome
#retorna o nome da categoria para facil visualização

#O models.CharField é o tipo de campo mais fundamental do Django para armazenar texto de comprimento curto a médio no banco de dados.
class Equipamento(models.Model):
    status_escolha = [
    ('EM_USO', 'Em uso'),
    ('ESTOQUE', 'Estoque'),
    ('MANUTENCAO', 'Manutenção'),
    ]
    nome = models.CharField(max_length=200)
    serial = models.CharField(max_length=100, unique=True)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=15,
        choices = status_escolha,
        default ='EM_USO'
    )

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        # Retorna uma representação útil, combinando nome e serial.
        return f"{self.nome} ({self.serial})"