"""
Rotas iniciais da API.
"""

from fastapi import APIRouter

from app.core.config import settings


# Agrupa os endpoints da API.
router = APIRouter()


@router.get("/health", tags=["Monitoramento"])
def health_check():
    """
    Verifica se a API está respondendo.

    Este endpoint será útil para testes e monitoramento.
    """

    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
    }