# 🛒 E-commerce Full-Stack (Django + JavaScript)

Protótipo de loja virtual com **back-end em Django** e **front-end dinâmico**. Desenvolvido para praticar integração entre sistemas e lógica de e-commerce.

## 🚀 Funcionalidades

### Back-End (Django)
- **Modelagem de dados**: 
  - `Produto`: nome, preço, descrição, imagem (via `ImageField`).
  - `Carrinho`: sessão de compras com relacionamento entre usuário e produtos.
- **Views**:
  - API para listar produtos (serialização com `JsonResponse`).
  - Endpoints para adicionar/remover itens do carrinho.
- **Admin Django**: Painel para gerenciar produtos.

### Front-End (HTML/CSS)
- **Carrinho dinâmico**:
  - Adicionar/remover itens sem recarregar a página (`fetch` ou AJAX).
  - Cálculo automático do total.
- **Responsividade**: Layout adaptável (mobile/desktop) com CSS Flexbox.

## 🔧 Tecnologias

| Back-End       | Front-End      | Ferramentas     |
|----------------|----------------|----------------|
| Python 3       | HTML5          | Git            |
| Django 4.x     | CSS3           | SQLite         |
| Django ORM     |BootStrap       | VS Code        |

## 📦 Como Executar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/cauecaramello/ecommerce.git
   cd web
