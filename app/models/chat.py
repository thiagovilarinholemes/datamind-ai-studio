"""
====================================================================
CHAT MODELS
====================================================================

Modelos Pydantic utilizados pelo Chat do DataMind AI Studio.

Provedores suportados:

    - Ollama
    - Hugging Face
====================================================================
"""

from typing import Literal

from pydantic import BaseModel, Field


# ================================================================
# PROVEDORES SUPORTADOS
# ================================================================

AIProvider = Literal[
    "ollama",
    "huggingface",
]


# ================================================================
# REQUEST
# ================================================================

class ChatRequest(BaseModel):
    """
    Dados recebidos pelo endpoint do Chat.

    Exemplo:

        {
            "provider": "ollama",
            "model": "qwen2.5-coder:3b",
            "message": "Explique o que é Kafka"
        }
    """

    provider: AIProvider = Field(
        default="ollama",
        description="Provedor de IA utilizado.",
    )

    model: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description=(
            "Modelo utilizado pelo provedor."
        ),
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description=(
            "Mensagem enviada pelo usuário."
        ),
    )


# ================================================================
# RESPONSE
# ================================================================

class ChatResponse(BaseModel):
    """
    Resposta tradicional do Chat.
    """

    response: str

    provider: AIProvider

    model: str | None = None
