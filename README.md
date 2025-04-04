# 🍱 Open Delivery API Demo / API de Cardápio e Pedidos

This is a demo project that simulates the integration of a restaurant with the [Open Delivery](https://abrasel-nacional.github.io/docs/) standard. It allows testing of menu creation, item offers, and order lifecycle.  
Este é um projeto de demonstração que simula a integração de um restaurante com o padrão Open Delivery. Permite testar a criação de cardápios, ofertas de itens e o ciclo completo de pedidos.

---

## 🚀 Technologies / Tecnologias

- FastAPI (Python)
- PostgreSQL
- SQLAlchemy + Alembic
- Docker + Docker Compose
- Pydantic

---

## 📂 Structure / Estrutura

```
app/
├── api/        # Endpoints
├── crud/       # Funções de banco
├── models/     # Modelos SQLAlchemy
├── schemas/    # Schemas Pydantic
├── utils/      # Funções auxiliares + mocks
alembic/        # Migrações
```

---

## 🌱 Environment / Ambiente

Copy file `.env.example` into `.env`:
Copie os arquivos `.env.example` para `.env`:

````bash
cp .env.example .env


## 🛠️ Setup (dev)

```bash
git clone https://github.com/ken-okubo/open-delivery-api-demo.git
cd open-delivery-api-demo
docker compose up -d
````

### Database Migration / Migração de Banco

To run alembic locally:
Para rodar alembic localmente:

```bash
export RUNNING_OUTSIDE_DOCKER=1
alembic upgrade head
```

To create new migration:
Para criar nova migration:

```bash
alembic revision --autogenerate -m "mensagem"
```

---

## 🧪 Mock Data

Run mock_data with:
Rode os dados de exemplo com:

```bash
docker compose exec web python -m app.utils.mock_data
```

It created categories, items, menus and orders for test.
Cria categorias, itens, menus e pedidos para testes.

---

## 🔗 API Docs

- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

---

## 📦 Exemplos de Requisição (curl)

```bash
# Lista menus / Listar menus
curl http://localhost:8000/menus/

# Create order / Criar pedido
curl -X POST http://localhost:8000/orders/ -H "Content-Type: application/json" -d @example_order.json
```

---

## 🤝 Contributing | Contribuindo

Suggestions and improvements are welcome!  
Sugestões e melhorias são bem-vindas!

---

## 🧠 Inspiration | Inspiração

I started this project to dive deeper into the Open Delivery standard and improve my skills with FastAPI, SQLAlchemy, Docker, and async Python.
It’s also a great opportunity to simulate a real-world API based on something I’m working on with iHungry company.

Comecei este projeto para me aprofundar no padrão Open Delivery e melhorar minhas habilidades com FastAPI, SQLAlchemy, Docker e Python assíncrono.
Também é uma boa oportunidade para simular uma API real baseada em algo que estou desenvolvendo com a empresa iHungry.

---

## 👤 Author | Autor

- [Ken Okubo on LinkedIn](https://www.linkedin.com/in/ken-okubo-8b484978/)
- [GitHub Profile](https://github.com/ken-okubo)
