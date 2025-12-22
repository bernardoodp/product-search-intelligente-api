# Nome do Seu Projeto

API de processamento assíncrono integrada com Magalu e Mercado Livre, usando Django e Celery.

## Como Rodar

Você pode rodar este projeto de duas formas: usando Docker (recomendado) ou instalando as dependências Manualmente.

### Opção 1: Usando Docker

#### Pré-requisitos
* Git
* Docker Desktop

#### Passo a Passo

1.  **Clone o repositório:**
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/seu-usuario/seu-projeto.git)
    cd seu-projeto
    

2.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto baseado no exemplo fornecido:
    cp .env.example .env

    *Se necessário, edite o arquivo `.env` para ajustar senhas, mas o padrão já funciona no Docker.*

3.  **Suba a aplicação:**
    Execute o comando abaixo para construir as imagens e iniciar os containers:
    docker compose up --build

4.  **Acesse:**
    * A API estará disponível em: `http://localhost:8000`
    * O Banco de Dados estará rodando na porta: `5433` (externamente)

---

### Opção 2: Instalação Manual (Tradicional)

#### Pré-requisitos
* Python 3.10+
* PostgreSQL (Instalado e rodando)
* Redis (Instalado e rodando)

#### Passo a Passo

1.  **Configure o Ambiente Virtual:**
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate

2.  **Instale as dependências:**
    pip install -r requirements.txt
    

3.  **Configure as Variáveis de Ambiente:**
    Crie o arquivo `.env`:
    cp .env.example .env

4.  **Execute as Migrações:**
    python manage.py migrate

5.  **Rode o Servidor (API):**
    python manage.py runserver

6.  **Rode o Celery (Worker):**
    Em um novo terminal (com a venv ativada), rode:
    # Windows/Linux/Mac
    python -m celery -A setup worker --loglevel=info

---

## ⚙️ Variáveis de Ambiente

As principais variáveis configuradas no `.env` são:

| Variável | Descrição | Padrão Docker | Padrão Manual |

| `DB_NAME` | Nome do Banco de Dados | `magaludb` | `magaludb` |
| `DB_USER` | Usuário do Banco | `magaluuser` | *seu user local* |
| `DB_PASSWORD` | Senha do Banco | `magalupass` | *sua senha local* |
| `DB_HOST` | Host do Banco | `db` | `localhost` |
| `DB_PORT` | Porta do Banco | `5432` | `5432` |
| `CELERY_BROKER_URL` | URL de conexão Redis | `redis://redis:6379/0` | `redis://localhost:6379/0` |