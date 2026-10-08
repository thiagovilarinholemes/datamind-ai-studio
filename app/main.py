
"""
Ponto de entrada da API FastAPI.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.routes import router
from app.api.routes.chat import router as chat_router

# Importar os modelos registra suas tabelas no metadata.
from app.database.connection import Base, engine
from app.database import models  # noqa: F401

from app.api.routes.models import router as models_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executa tarefas durante a inicialização da API.

    Nesta fase, cria as tabelas que ainda não existem.
    Posteriormente, utilizaremos Alembic para migrações.
    """

    Base.metadata.create_all(bind=engine)

    yield


# Cria a aplicação FastAPI.
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Plataforma de desenvolvimento de IA, agentes, "
        "Python, SQL e Engenharia de Dados."
    ),
    lifespan=lifespan,
)


# Registra as rotas existentes com o prefixo de versão.
app.include_router(
    router,
    prefix="/api/v1",
)


# Registra as rotas do Chat de IA.
app.include_router(
    chat_router,
    prefix="/api/v1",
)

app.include_router(
    models_router,
    prefix="/api/v1",
)


@app.get("/", tags=["Informações"])
def root():
    """
    Endpoint inicial para confirmar que a API está funcionando.
    """

    return {
        "message": f"{settings.app_name} está em execução."
    }