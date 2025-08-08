# Python FastAPI Live Coding - Social API

## Stack
- FastAPI
- SQLAlchemy (sync) + PostgreSQL
- Pydantic (DTOs)
- Faker (seed)
- Docker Compose (PostgreSQL)

## Rodando local
```bash
# 1) Clonar o repositório
# 2) Subir o banco
docker-compose up -d

# 3) Criar venv e instalar deps
python -m venv venv
source venv/Scripts/activate  # Windows Bash conforme combinado
pip install -r requirements.txt

# 4) Variáveis de ambiente
cp .env .env

# 5) Inicializar DB (tabelas)
python scripts/init_db.py

# 6) Rodar API
uvicorn app.main:app --reload
```

## Endpoints
- POST `/users` → cadastra usuário
- POST `/posts` → cria um post
- POST `/posts/{post_id}/like` → curtir
- GET `/feed?page=&size=` → feed paginado (recente primeiro)
- GET `/users-with-posts?page=&size=` → usuários com seus posts (paginação por usuários)

## Carga de teste
- `python scripts/seed.py --users 1000 --posts-per-user 1000 --batch 5000`
  - Gera 1000 usuários e **1.000.000** posts (em lotes).

## Observações
- Arquitetura Clean (domain, application, infrastructure, entrypoints, dtos)
- DTOs de entrada/saída, sem retornar entidades do ORM
- `app/main.py` ponto de entrada
