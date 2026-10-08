"""
====================================================================
DATAMIND AI STUDIO
SERVIÇO DE MODELOS
====================================================================

Responsável por descobrir os modelos disponíveis nos provedores
de IA utilizados pelo DataMind AI Studio.

Atualmente:

    Ollama
    Hugging Face
====================================================================
"""

import os

import requests


# ====================================================================
# CONFIGURAÇÕES
# ====================================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
).rstrip("/")


# ====================================================================
# MODELOS HUGGING FACE
# ====================================================================

# Por enquanto o Hugging Face utiliza um catálogo configurável.
#
# Posteriormente podemos transformar isso em um catálogo mais
# completo ou buscar modelos de uma API externa.

HUGGINGFACE_MODELS = [
    "openai/gpt-oss-120b",
]


# ====================================================================
# OLLAMA
# ====================================================================

def get_ollama_models() -> list[str]:
    """
    Consulta o Ollama e retorna os modelos instalados.

    Endpoint utilizado:

        GET /api/tags

    Retorna apenas os nomes dos modelos.
    """

    response = requests.get(
        f"{OLLAMA_URL}/api/tags",
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    models = data.get("models", [])

    return [
        model.get("name")
        for model in models
        if model.get("name")
    ]


# ====================================================================
# HUGGING FACE
# ====================================================================

def get_huggingface_models() -> list[str]:
    """
    Retorna os modelos configurados para Hugging Face.
    """

    return HUGGINGFACE_MODELS.copy()
