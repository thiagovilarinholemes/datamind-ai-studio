"""
====================================================================
OLLAMA SERVICE
====================================================================

Responsável pela comunicação com o Ollama.

Funções:

    generate_with_ollama()
        Retorna a resposta completa.

    stream_with_ollama()
        Retorna a resposta progressivamente.

====================================================================
"""

import json
import os
from collections.abc import Generator

import requests


# URL do servidor Ollama.
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
).rstrip("/")


# Modelo utilizado pelo Ollama.
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5-coder:3b",
)


def build_payload(
    message: str,
    system_prompt: str,
    stream: bool,
) -> dict:
    """
    Monta o payload enviado ao Ollama.

    Manter essa construção em uma função evita duplicação
    entre o modo normal e o modo streaming.
    """

    return {
        "model": OLLAMA_MODEL,
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
            # Temperatura baixa para respostas técnicas
            # mais consistentes.
            "temperature": 0.3,

            # Limite de geração.
            "num_predict": 1024,
        },
    }


def generate_with_ollama(
    message: str,
    system_prompt: str,
) -> str:
    """
    Gera uma resposta completa através do Ollama.

    Esse método continua disponível para endpoints
    que não utilizam streaming.
    """

    url = f"{OLLAMA_URL}/api/chat"

    payload = build_payload(
        message=message,
        system_prompt=system_prompt,
        stream=False,
    )

    response = requests.post(
        url,
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    data = response.json()

    content = (
        data
        .get("message", {})
        .get("content", "")
        .strip()
    )

    if not content:
        raise RuntimeError(
            "O Ollama não retornou conteúdo."
        )

    return content


def stream_with_ollama(
    message: str,
    system_prompt: str,
) -> Generator[str, None, None]:
    """
    Gera a resposta progressivamente através do Ollama.

    O Ollama envia vários objetos JSON durante a geração.
    Cada objeto pode conter um pequeno trecho da resposta.

    A função extrai somente:

        message.content

    e entrega esse trecho imediatamente ao FastAPI.
    """

    url = f"{OLLAMA_URL}/api/chat"

    payload = build_payload(
        message=message,
        system_prompt=system_prompt,
        stream=True,
    )

    try:

        with requests.post(
            url,
            json=payload,
            stream=True,
            timeout=180,
        ) as response:

            response.raise_for_status()

            # O Ollama envia uma linha JSON por evento.
            for line in response.iter_lines(
                decode_unicode=True,
            ):

                if not line:
                    continue

                try:
                    data = json.loads(line)

                except json.JSONDecodeError:
                    # Ignora linhas inválidas sem derrubar
                    # toda a resposta.
                    continue

                content = (
                    data
                    .get("message", {})
                    .get("content", "")
                )

                if content:
                    yield content

                # Quando o Ollama informa que terminou,
                # encerramos o gerador.
                if data.get("done") is True:
                    break

    except requests.RequestException as exc:

        raise RuntimeError(
            f"Erro ao comunicar com o Ollama: {exc}"
        ) from exc
