import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from .forms import CursoForm
from .forms import CompraCursoForm
from .forms import UsuarioForm
from .forms import FotoForm
from .models import Curso
from .models import Venda
from .models import Usuario

def index(request):
    return render(request, 'app/index.html')

def cadastrar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso criado com sucesso!")
            return redirect('cursos')
    else:
        form = CursoForm()

    return render(request, 'app/cadastrar_curso.html', {'form': form})

def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'app/cursos.html', {'cursos': cursos})

def excluir_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.delete()
    return redirect('cursos')

def comprar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 0))

        if quantidade <= 0:
            messages.error(request, "Quantidade inválida.")
            return redirect('comprar_curso', curso_id=curso.id)
        if quantidade > curso.quantidade_estoque:
            messages.error(request, "Estoque insuficiente para esta compra.")
            return redirect('comprar_curso', curso_id=curso.id)

        curso.quantidade_estoque -= quantidade
        curso.save()

        venda = Venda(
            usuario=request.user,
            curso=curso,
            quantidade=quantidade,
            valor_total=curso.preco * quantidade
        )
        venda.save()

        messages.success(request, f"Compra realizada com sucesso! Você comprou {quantidade} curso(s) de {curso.nome}.")
        return redirect('cursos') 

    return render(request, 'app/comprar_curso.html', {'curso': curso})

@login_required
def listar_compras(request):
    compras = Venda.objects.filter(usuario=request.user)  # Filtra pelas compras do usuário logado
    return render(request, 'app/listar_compras.html', {'compras': compras})

@login_required
def grafico_vendas(request):

    vendas = Venda.objects.values('curso__nome').annotate(total=Sum('quantidade')).order_by('-total')
    cursos = [venda['curso__nome'] for venda in vendas]
    totais = [venda['total'] for venda in vendas]

    plt.figure(figsize=(8, 6))
    plt.bar(cursos, totais, color='skyblue')
    plt.xlabel('Cursos')
    plt.ylabel('Quantidade Vendida')
    plt.title('Gráfico de Vendas de Cursos')
    plt.xticks(rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagem_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return render(request, 'app/grafico_vendas.html', {'grafico': imagem_base64})

def cadastrar_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        foto = request.FILES.get('foto')  # Obtém a foto enviada pelo usuário

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('cadastrar_usuario')

        # Verificar se o e-mail já está cadastrado
        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return redirect('cadastrar_usuario')

        # Criar o usuário com a foto
        usuario = get_user_model()(
            email=email,
            username=email,  # Definindo o e-mail como o username
            password=make_password(senha),
            foto=foto  # Atribuindo a foto do formulário
        )
        usuario.save()

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')

    return render(request, 'app/cadastrar_usuario.html')

def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('login')
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('login')
        
        user = authenticate(request, username=usuario.username, password=senha)

        if user is not None:
            login(request, user)  # Logar o usuário
            return redirect('dashboard')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('login')

    return render(request, 'app/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmacao_senha = request.POST.get('confirmacao_senha')

        if not request.user.check_password(senha_atual):
            messages.error(request, "A senha atual está incorreta.")
        elif nova_senha != confirmacao_senha:
            messages.error(request, "A nova senha e a confirmação não coincidem.")
        else:
            request.user.set_password(nova_senha)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('dashboard')

    return render(request, 'app/alterar_senha.html')

@login_required
def excluir_conta(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Conta excluída com sucesso!")
        return redirect('index')
    return render(request, 'app/excluir_conta.html')

@login_required
def adicionar_foto(request):
    usuario = request.user
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto atualizada com sucesso!')
            return redirect('dashboard')
    else:
        form = FotoForm(instance=usuario)
    return render(request, 'app/adicionar_foto.html', {'form': form})

def galeria(request):
    usuarios = Usuario.objects.all()
    cursos = Curso.objects.exclude(foto='')
    return render(request, 'app/galeria.html', {'usuarios': usuarios, 'cursos': cursos})

def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        send_mail(
            f'Contato de {nome}',
            mensagem,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        messages.success(request, "Mensagem enviada com sucesso!")
        return redirect('contato')
    return render(request, 'app/contato.html')