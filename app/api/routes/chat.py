"""
====================================================================
CHAT ROUTER
====================================================================

Endpoints responsáveis pelo Chat do DataMind AI Studio.

Endpoints:

    POST /api/v1/chat

    POST /api/v1/chat/stream
====================================================================
"""

from collections.abc import Generator

from fastapi import APIRouter, HTTPException

from fastapi.responses import StreamingResponse

from app.models.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.ai_provider import (
    generate_response,
    get_default_model,
    normalize_provider,
    stream_response,
)


# ================================================================
# ROUTER
# ================================================================

router = APIRouter(
    prefix="/chat",
    tags=["Chat IA"],
)


# ================================================================
# CHAT NORMAL
# ================================================================

@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    try:

        selected_provider = normalize_provider(
            request.provider
        )

        selected_model = (
            request.model
            if request.model
            else get_default_model(
                selected_provider
            )
        )


        response = generate_response(
            message=request.message,
            provider=selected_provider,
            model=selected_model,
        )


        return ChatResponse(
            response=response,
            provider=selected_provider,
            model=selected_model,
        )


    except Exception as exc:

        print(
            f"[Chat Error] {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Erro ao consultar "
                f"o modelo de IA: {exc}"
            ),
        ) from exc


# ================================================================
# CHAT STREAMING
# ================================================================

@router.post(
    "/stream",
)
def chat_stream(
    request: ChatRequest,
):

    def generate() -> Generator[str, None, None]:

        try:

            yield from stream_response(
                message=request.message,
                provider=request.provider,
                model=request.model,
            )

        except Exception as exc:

            print(
                f"[Chat Streaming Error] {exc}"
            )

            yield (
                f"\n\n[ERRO] {exc}"
            )


    return StreamingResponse(
        generate(),
        media_type=(
            "text/plain; "
            "charset=utf-8"
        ),
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
