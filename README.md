## 🧠 Where Are You From, Really? – Tech Task Solution

This repository is a solution for the Python Junior Tech Task.
It is a Django-based service that predicts a person's likely country of origin based on their name using external APIs, enriches that data, stores it, and provides endpoints for querying.

## 🚀 Stack
  - Django
  - Django Ninja – Lightweight FastAPI-like API framework for Django
  - PostgreSQL
  - Docker / Docker Compose
  - Pytest – For integration and E2E testing
  - Ruff – For linting and formatting
  - Swagger UI – Auto-generated API docs via Django Ninja

## 📦 Setup & Installation

1. Clone the repo
```bash
git clone https://github.com/KERELKO/valth-solutions-test-task
cd valth-solutions-test-task
```
2. Create .env file
You can copy the provided `.env.template` and adjust as needed:
```bash
cp .env.template .env
```
⚙️ .env Variables
```bash
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTRES_NAME=postgres
DJANGO_SETTINGS_MODULE=location_finder.core.settings
```
4. Start the project with Docker
```bash
docker compose up --build
```
On the first launch you need to apply all migrations for the database. You can do it manually
with `docker exec -it <app_container> python manage.py migrate` or with make command: `make migrate`

The project also has `Makefile` with useful commands
```bash
make up                # docker compose up --build
make makemigrations    # create new migrations
make migrate           # apply migrations
make createsuperuser   # create a Django superuser
```
5. Access the API
Docs: http://localhost:8000/api/docs

## 🔌 API Endpoints
### __/names/?name=John__
#### Predicts nationality from a given name.
* Uses cache if last_accessed_at is within 1 day.
* Returns country metadata from local DB or fetches it if not present.

#### Error Responses
```http
400 Bad Request – Missing name

404 Not Found – No countries found
```

### /popular-names/?country=US
#### Returns top 5 names most frequently associated with a given country.

#### Error Responses
```http
400 Bad Request – Missing country

404 Not Found – No names for country
```

### 🛠 Improvements & Technical Decisions
#### ✅ Improvements
  * Replaced Django Rest Framework with Django Ninja to benefit from FastAPI-like syntax while retaining Django's ORM and Admin features.

## ✅ Tests
Run all tests with:
```bash
make tests
```
The project empowered with __integrations__ and __edge-to-edge__ tests

### 🧹 Code Quality
Lint and format using pre-commit:
```
ruff check .
ruff format .
```
### 📌 TODOs / Future Enhancements
  - Add pagination for /names/ if more countries are supported
  - Caching layer (e.g., Redis) for repeated queries
  - Background workers to prefetch country metadata
