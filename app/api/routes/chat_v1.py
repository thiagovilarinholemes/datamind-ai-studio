"""
====================================================================
CHAT ROUTER
====================================================================

Endpoints relacionados ao Chat de IA.

Endpoints:

    POST /chat
        Retorna a resposta completa.

    POST /chat/stream
        Retorna a resposta progressivamente.

====================================================================
"""

from collections.abc import Generator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.ai_provider import (
    generate_response,
    stream_response,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat IA"],
)


class ChatRequest(BaseModel):
    """
    Dados recebidos pelo Chat.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Mensagem enviada pelo usuário.",
    )


class ChatResponse(BaseModel):
    """
    Resposta tradicional da API.
    """

    response: str


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    """
    Endpoint tradicional.

    Retorna a resposta completa em JSON.
    """

    try:

        response = generate_response(
            message=request.message,
        )

        return ChatResponse(
            response=response,
        )

    except Exception as exc:

        print(
            f"[Chat Error] {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Erro ao consultar o modelo de IA: "
                f"{exc}"
            ),
        ) from exc


@router.post(
    "/stream",
)
def chat_stream(
    request: ChatRequest,
):
    """
    Endpoint de streaming.

    Cada trecho gerado pelo modelo é enviado
    imediatamente ao cliente.
    """

    def generate() -> Generator[str, None, None]:
        """
        Gerador responsável por encaminhar os
        pedaços da resposta.
        """

        try:

            yield from stream_response(
                message=request.message,
            )

        except Exception as exc:

            print(
                f"[Chat Streaming Error] {exc}"
            )

            yield (
                "\n\n[ERRO] "
                f"{exc}"
            )

    return StreamingResponse(
        generate(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
