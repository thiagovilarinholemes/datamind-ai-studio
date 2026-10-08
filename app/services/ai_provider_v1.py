"""
====================================================================
AI PROVIDER
====================================================================

Controlador dos provedores de Inteligência Artificial.

Provedores:

    - Ollama
    - Hugging Face

Também disponibiliza streaming para o Chat.

====================================================================
"""

import os
from collections.abc import Generator

from app.services.ollama_service import (
    generate_with_ollama,
    stream_with_ollama,
)


# Provedor atualmente configurado.
AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "ollama",
).lower()


# Prompt principal do DataMind.
DEFAULT_SYSTEM_PROMPT = """
Você é o assistente oficial do DataMind AI Studio.

Responda sempre em português do Brasil.

Seu objetivo é auxiliar o usuário em:

- Python
- SQL
- Engenharia de Dados
- Ciência de Dados
- Machine Learning
- Inteligência Artificial
- Agentes de IA
- Docker
- Kafka
- Airflow
- Apache Spark
- PostgreSQL
- APIs
- FastAPI
- Hugging Face
- Ollama
- Flet

Regras:

1. Explique conceitos técnicos de forma clara e didática.

2. Quando fornecer código, entregue código completo.

3. Nunca interrompa um bloco de código.

4. Utilize boas práticas de programação.

5. Utilize comentários no código quando forem úteis.

6. Quando o usuário solicitar alteração em um arquivo,
   apresente o arquivo completo corrigido.

7. Não invente informações técnicas.

8. Quando houver mais de uma solução possível,
   explique brevemente as alternativas.

9. Priorize exemplos práticos.

10. Responda de maneira organizada utilizando títulos,
    listas e blocos de código quando apropriado.
"""


def generate_response(
    message: str,
    system_prompt: str | None = None,
) -> str:
    """
    Gera uma resposta completa.
    """

    final_system_prompt = (
        system_prompt
        if system_prompt
        else DEFAULT_SYSTEM_PROMPT
    )

    if AI_PROVIDER == "ollama":

        print(
            "[AI Provider] Ollama -> "
            f"{os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:3b')}"
        )

        return generate_with_ollama(
            message=message,
            system_prompt=final_system_prompt,
        )

    if AI_PROVIDER == "huggingface":

        from app.services.huggingface_service import (
            generate_with_huggingface,
        )

        print(
            "[AI Provider] Hugging Face"
        )

        return generate_with_huggingface(
            message=message,
            system_prompt=final_system_prompt,
        )

    raise ValueError(
        "AI_PROVIDER inválido. "
        "Utilize 'ollama' ou 'huggingface'."
    )


def stream_response(
    message: str,
    system_prompt: str | None = None,
) -> Generator[str, None, None]:
    """
    Gera uma resposta progressivamente.

    Atualmente o streaming está implementado para Ollama.

    Cada trecho recebido do modelo é imediatamente
    encaminhado para o FastAPI.
    """

    final_system_prompt = (
        system_prompt
        if system_prompt
        else DEFAULT_SYSTEM_PROMPT
    )

    if AI_PROVIDER == "ollama":

        print(
            "[AI Provider] Ollama Streaming -> "
            f"{os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:3b')}"
        )

        yield from stream_with_ollama(
            message=message,
            system_prompt=final_system_prompt,
        )

        return

    if AI_PROVIDER == "huggingface":

        raise NotImplementedError(
            "Streaming para Hugging Face ainda "
            "será implementado."
        )

    raise ValueError(
        "AI_PROVIDER inválido. "
        "Utilize 'ollama' ou 'huggingface'."
    )
