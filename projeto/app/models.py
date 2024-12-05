from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    duracao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField(default=0)
    foto = models.ImageField(upload_to='cursos/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Venda(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_compra = models.DateTimeField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        curso = self.curso
        curso.quantidade_estoque -= self.quantidade
        if curso.quantidade_estoque < 0:
            raise ValueError("Não há estoque suficiente para esta compra")
        curso.save()
        self.valor_total = curso.preco * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de {self.curso.nome} para {self.usuario.username} em {self.data_compra}"

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username