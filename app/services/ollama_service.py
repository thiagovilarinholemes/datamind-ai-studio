"""
====================================================================
OLLAMA SERVICE
====================================================================

Integração do DataMind AI Studio com o Ollama.

O Ollama deve estar disponível na rede Docker.

Exemplo:

    http://ollama:11434

Endpoints utilizados:

    POST /api/chat

Funcionalidades:

    - Geração normal
    - Streaming
    - Seleção dinâmica do modelo
====================================================================
"""

import json
import os
from collections.abc import Generator

import requests


# ================================================================
# CONFIGURAÇÕES
# ================================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
).rstrip("/")


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5-coder:3b",
)


# ================================================================
# PAYLOAD
# ================================================================

def build_payload(
    message: str,
    system_prompt: str,
    model: str | None = None,
    stream: bool = False,
) -> dict:

    selected_model = (
        model
        if model
        else OLLAMA_MODEL
    )

    return {
        "model": selected_model,

        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": message,
            },
        ],

        "stream": stream,

        "options": {
            "temperature": 0.3,
            "num_predict": 1024,
        },
    }


# ================================================================
# GERAÇÃO NORMAL
# ================================================================

def generate_with_ollama(
    message: str,
    system_prompt: str,
    model: str | None = None,
) -> str:

    selected_model = (
        model
        if model
        else OLLAMA_MODEL
    )

    print(
        f"[Ollama] Modelo: "
        f"{selected_model}"
    )


    payload = build_payload(
        message=message,
        system_prompt=system_prompt,
        model=selected_model,
        stream=False,
    )


    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        timeout=180,
    )


    response.raise_for_status()


    data = response.json()


    content = (
        data
        .get("message", {})
        .get("content", "")
    )


    if not content:

        raise RuntimeError(
            "Ollama retornou uma resposta vazia."
        )


    return content.strip()


# ================================================================
# STREAMING
# ================================================================

def stream_with_ollama(
    message: str,
    system_prompt: str,
    model: str | None = None,
) -> Generator[str, None, None]:

    selected_model = (
        model
        if model
        else OLLAMA_MODEL
    )

    print(
        f"[Ollama Streaming] "
        f"Modelo: {selected_model}"
    )


    payload = build_payload(
        message=message,
        system_prompt=system_prompt,
        model=selected_model,
        stream=True,
    )


    with requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        stream=True,
        timeout=300,
    ) as response:

        response.raise_for_status()


        for line in response.iter_lines(
            decode_unicode=True,
        ):

            if not line:
                continue


            try:

                data = json.loads(line)


                content = (
                    data
                    .get("message", {})
                    .get("content", "")
                )


                if content:

                    yield content


                if data.get("done"):

                    break


            except json.JSONDecodeError:

                continue
