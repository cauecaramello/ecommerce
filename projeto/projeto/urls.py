from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cadastrar_curso/', views.cadastrar_curso, name='cadastrar_curso'),
    path('cursos/', views.lista_cursos, name='cursos'),
    path('comprar_curso/<int:curso_id>/', views.comprar_curso, name='comprar_curso'),
    path('excluir_curso/<int:curso_id>/', views.excluir_curso, name='excluir_curso'),
    path('grafico_vendas/', views.grafico_vendas, name='grafico_vendas'),
    path('compras/', views.listar_compras, name='listar_compras'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('excluir_conta/', views.excluir_conta, name='excluir_conta'),
    path('galeria/', views.galeria, name='galeria'),
    path('adicionar_foto/', views.adicionar_foto, name='adicionar_foto'),
    path('contato/', views.contato, name='contato'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
