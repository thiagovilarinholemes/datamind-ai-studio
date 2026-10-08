"""
====================================================================
DATAMIND AI STUDIO
ROTAS DE MODELOS
====================================================================

Endpoints responsáveis por informar ao frontend quais modelos estão
disponíveis em cada provedor de IA.
====================================================================
"""

from fastapi import APIRouter, HTTPException

from app.services.model_service import (
    get_huggingface_models,
    get_ollama_models,
)


# ====================================================================
# ROUTER
# ====================================================================

router = APIRouter(
    prefix="/models",
    tags=["Modelos de IA"],
)


# ====================================================================
# OLLAMA
# ====================================================================

@router.get("/ollama")
def ollama_models():
    """
    Retorna os modelos instalados no Ollama.
    """

    try:

        models = get_ollama_models()

        return {
            "provider": "ollama",
            "models": models,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Não foi possível consultar o Ollama: {exc}",
        ) from exc


# ====================================================================
# HUGGING FACE
# ====================================================================

@router.get("/huggingface")
def huggingface_models():
    """
    Retorna os modelos configurados para Hugging Face.
    """

    try:

        models = get_huggingface_models()

        return {
            "provider": "huggingface",
            "models": models,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar modelos Hugging Face: {exc}",
        ) from exc
