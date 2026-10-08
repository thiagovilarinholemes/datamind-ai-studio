# DataMind AI Studio

Plataforma de desenvolvimento assistido por IA para Python,
SQL, agentes inteligentes e Engenharia de Dados.

## Objetivo

Construir uma aplicação modular com interface gráfica, API,
persistência de conversas e integração progressiva com modelos
Hugging Face e ferramentas de Engenharia de Dados.

## Stack inicial

- Python 3.12
- FastAPI
- Uvicorn
- Flet
- PostgreSQL 16
- SQLAlchemy 2
- Docker
- Docker Compose
- Pytest

## Estrutura

- `app/`: API, configurações e acesso ao banco.
- `frontend/`: interface Flet.
- `tests/`: testes automatizados.

## Requisitos

- Windows 11
- Docker Desktop com integração WSL 2 habilitada
- Python 3.12
- VS Code (recomendado)

## Configuração

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

# Endereços URL
```yaml
API: http://localhost:8000 
Swagger: http://localhost:8000/docs 
Health check: http://localhost:8000/api/v1/health 
PostgreSQL no host: localhost:5433
```

Crie o arquivo local de configuração:
```yaml
Copy-Item .env.example .env
```

## Iniciar os serviços
```yaml
docker compose up --build -d
```

Verifique os contêineres:
```yaml
docker compose ps
```

Consulte os logs da API:
```yaml
docker compose logs -f api
```

Executar a API localmente

Crie um ambiente virtual:
```yaml
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure a URL do banco para acesso pelo Windows:
```yaml
$env:DATABASE_URL = "postgresql+psycopg://datamind:datamind_dev@localhost:5433/datamind"
uvicorn app.main:app --reload
Executar os testes
pytest -q
```