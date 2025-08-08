# Python FastAPI Livecoding – Social API

API desenvolvida durante teste de live coding (tempo oficial: **2h**) seguindo **Clean Architecture**, princípios **DDD** e **SOLID**.  
Implementada com **FastAPI**, **PostgreSQL** e **SQLAlchemy**, inclui tratamento de erros, seed massivo com **1.000.000** de posts e testes unitários.

---

## 📌 Funcionalidades

### 1. Cadastro de Usuários
- **Endpoint**: `POST /users`
- **Request**:
```json
{ "username": "alice", "email": "alice@test.com", "posts": 0 }
```
- **Response**:
```json
{ "id": 1, "username": "alice" }
```
- **Validações**:
  - `username` mínimo 3 caracteres, máximo 50.
  - `email` válido (validação Pydantic).
  - Retorna **409 Conflict** para:
    - Email já existente → `"Email already exists"`.
    - Username já existente → `"Username already exists"`.

### 2. Criar Post
- **Endpoint**: `POST /posts`
- **Request**:
```json
{ "user_id": 1, "content": "Hello world" }
```
- **Response**:
```json
{
  "id": 1,
  "user_id": 1,
  "content": "Hello world",
  "likes": 0,
  "created_at": "2025-08-02T12:00:00Z"
}
```
- **Validações**:
  - `user_id` deve existir.
  - `content` mínimo 1 e máximo 500 caracteres.

### 3. Curtir Post
- **Endpoint**: `POST /posts/{post_id}/like`
- Incrementa contador de likes.
- Retorna 404 se não existe.

### 4. Listar Feed de Postagens
- **Endpoint**: `GET /feed?page=&size=`
- Ordenação: mais recentes primeiro (`created_at DESC, id DESC`).
- Paginação configurável.
- Retorna:
```json
{
  "page": 1,
  "size": 5,
  "total": 1000000,
  "items": [ ... ]
}
```

### 5. Listar Usuários com seus Posts
- **Endpoint**: `GET /users-with-posts?page=&size=`
- Retorna cada usuário com todos os seus posts.
- Paginação sobre usuários.
- Implementado com `selectinload` para evitar N+1 queries.

### 6. Seed Massivo de Dados
- **Script**: `scripts/seed.py`
- Usa **Faker** para gerar dados realistas.
- Gera **1000 usuários** × **1000 posts cada** = **1.000.000 posts**.
- Execução otimizada em lotes (`batch`) para performance.

---

## 🛠 Tecnologias & Arquitetura
- **FastAPI** (framework web rápido e tipado)
- **PostgreSQL** (banco relacional robusto e escalável)
- **SQLAlchemy 2.0** (ORM com tipagem moderna)
- **Pydantic** (validação de dados)
- **Faker** (geração de dados fake)
- **Pytest + HTTPX** (testes unitários e de integração)
- **Docker Compose** (orquestração local)

---

## 🚀 Como executar localmente

### 1. Clonar repositório
```bash
git clone https://github.com/victorbfcastro/python-fastapi-livecoding.git
cd python-fastapi-livecoding
```

### 2. Subir PostgreSQL
```bash
docker-compose up -d
```

### 3. Criar ambiente virtual e instalar dependências
```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

### 4. Configurar variáveis
```bash
cp .env.example .env
# Editar .env se necessário
```

### 5. Inicializar banco
```bash
python -m scripts.init_db
```

### 6. Rodar API
```bash
uvicorn app.main:app --reload
```
Acesse: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📊 Gerar dados de teste
```bash
python -m scripts.seed --users 1000 --posts-per-user 1000 --batch 5000
```
> Tempo médio local: ~2min30s para 1 milhão de posts.

---

## ⚡ Testes
```bash
pytest -q
```

---

## 💡 Justificativa da escolha pelo PostgreSQL
Optamos pelo **PostgreSQL** por ser:
1. **Escalável**: suporta partitioning (horizontal/vertical) e sharding.
2. **Consultas avançadas**: permite criar **materialized views** para feeds ou relatórios, reduzindo tempo de resposta em cenários de alto tráfego.
3. **Índices avançados**: suporte a **GIN**, **BRIN**, índices compostos e parciais para otimizar consultas por `user_id`, `created_at` etc.
4. **Robustez e integridade**: constraints (`UNIQUE`, `FK`) garantem consistência, fundamental para relacionamentos de usuários e posts.
5. **Facilidade de migração**: integrável com ferramentas como **Alembic** para versionamento de schema.

> Em um cenário real de alto volume, o feed poderia ser acelerado usando **partitioning por intervalo de datas** e **materialized views** atualizadas periodicamente, permitindo consultas rápidas mesmo com bilhões de registros.

---

## 📜 Estrutura de pastas
```
app/
├── application/       # Casos de uso (services de aplicação)
├── domain/            # Entidades e interfaces de domínio
├── dtos/              # DTOs de entrada e saída
├── entrypoints/       # Camada de apresentação (rotas HTTP)
├── infrastructure/    # DB, repositórios concretos
scripts/               # utilitários (init_db, seed)
tests/                 # testes unitários
```
