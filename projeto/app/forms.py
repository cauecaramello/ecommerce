from django import forms
from .models import Curso
from .models import Venda
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'autor', 'duracao', 'preco', 'foto', 'quantidade_estoque']
        widgets = {
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
        }

class CompraCursoForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['curso', 'quantidade']

    curso = forms.ModelChoiceField(queryset=Curso.objects.filter(quantidade_estoque__gt=0))
    quantidade = forms.IntegerField(min_value=1, max_value=10)

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'foto']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class FotoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto']