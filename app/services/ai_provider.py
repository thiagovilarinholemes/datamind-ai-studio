"""
====================================================================
AI PROVIDER
====================================================================

Camada central responsável por selecionar o provedor de IA.

Provedores suportados:

    - Ollama
    - Hugging Face

A seleção pode ser feita:

    1. Por requisição:
       provider="ollama"
       provider="huggingface"

    2. Pela variável de ambiente AI_PROVIDER,
       utilizada como fallback.

O mesmo princípio vale para o modelo.

====================================================================
"""

import os
from collections.abc import Generator

from app.services.ollama_service import (
    generate_with_ollama,
    stream_with_ollama,
)
from app.services.huggingface_service import (
    generate_with_huggingface,
)


# ==================================================================
# CONFIGURAÇÃO PADRÃO
# ==================================================================

# Provedor utilizado quando a requisição não informa
# explicitamente qual provedor deseja utilizar.
DEFAULT_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "ollama",
).lower()


# Modelo padrão do Ollama.
DEFAULT_OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5-coder:3b",
)


# Modelo padrão do Hugging Face.
DEFAULT_HUGGINGFACE_MODEL = os.getenv(
    "HF_MODEL",
    "openai/gpt-oss-120b",
)


# ==================================================================
# SYSTEM PROMPT
# ==================================================================

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


# ==================================================================
# FUNÇÕES AUXILIARES
# ==================================================================

def normalize_provider(
    provider: str | None,
) -> str:
    """
    Normaliza o nome do provedor.

    Quando provider não é informado, utiliza
    o provedor definido em AI_PROVIDER.
    """

    selected_provider = (
        provider
        if provider
        else DEFAULT_PROVIDER
    )

    return selected_provider.strip().lower()


def get_default_model(
    provider: str,
) -> str:
    """
    Retorna o modelo padrão de acordo com o provedor.
    """

    if provider == "ollama":

        return DEFAULT_OLLAMA_MODEL

    if provider == "huggingface":

        return DEFAULT_HUGGINGFACE_MODEL

    raise ValueError(
        "AI_PROVIDER inválido. "
        "Utilize 'ollama' ou 'huggingface'."
    )


# ==================================================================
# GERAÇÃO DE RESPOSTA
# ==================================================================

def generate_response(
    message: str,
    provider: str | None = None,
    model: str | None = None,
    system_prompt: str | None = None,
) -> str:
    """
    Gera uma resposta utilizando o provedor selecionado.

    Parameters
    ----------
    message:
        Pergunta enviada pelo usuário.

    provider:
        Provedor desejado.

        Valores aceitos:

            ollama
            huggingface

        Se não informado, utiliza AI_PROVIDER.

    model:
        Modelo desejado.

        Se não informado, utiliza o modelo padrão
        configurado para o provedor.

    system_prompt:
        Prompt de sistema opcional.

    Returns
    -------
    str
        Resposta completa do modelo.
    """

    # --------------------------------------------------------------
    # Define o provedor
    # --------------------------------------------------------------

    selected_provider = normalize_provider(
        provider
    )


    # --------------------------------------------------------------
    # Define o modelo
    # --------------------------------------------------------------

    selected_model = (
        model
        if model
        else get_default_model(
            selected_provider
        )
    )


    # --------------------------------------------------------------
    # Define o System Prompt
    # --------------------------------------------------------------

    final_system_prompt = (
        system_prompt
        if system_prompt
        else DEFAULT_SYSTEM_PROMPT
    )


    # ==============================================================
    # OLLAMA
    # ==============================================================

    if selected_provider == "ollama":

        print(
            "[AI Provider] Ollama -> "
            f"{selected_model}"
        )

        return generate_with_ollama(
            message=message,
            system_prompt=final_system_prompt,
            model=selected_model,
        )


    # ==============================================================
    # HUGGING FACE
    # ==============================================================

    if selected_provider == "huggingface":

        print(
            "[AI Provider] Hugging Face -> "
            f"{selected_model}"
        )

        return generate_with_huggingface(
            message=message,
            system_prompt=final_system_prompt,
            model=selected_model,
        )


    # ==============================================================
    # PROVEDOR INVÁLIDO
    # ==============================================================

    raise ValueError(
        "Provedor de IA inválido. "
        "Utilize 'ollama' ou 'huggingface'."
    )


# ==================================================================
# STREAMING
# ==================================================================

def stream_response(
    message: str,
    provider: str | None = None,
    model: str | None = None,
    system_prompt: str | None = None,
) -> Generator[str, None, None]:
    """
    Gera uma resposta progressivamente.

    Atualmente o streaming está implementado para Ollama.

    Hugging Face será tratado posteriormente na Fase 3.
    """

    # --------------------------------------------------------------
    # Define o provedor
    # --------------------------------------------------------------

    selected_provider = normalize_provider(
        provider
    )


    # --------------------------------------------------------------
    # Define o modelo
    # --------------------------------------------------------------

    selected_model = (
        model
        if model
        else get_default_model(
            selected_provider
        )
    )


    # --------------------------------------------------------------
    # Define o System Prompt
    # --------------------------------------------------------------

    final_system_prompt = (
        system_prompt
        if system_prompt
        else DEFAULT_SYSTEM_PROMPT
    )


    # ==============================================================
    # OLLAMA
    # ==============================================================

    if selected_provider == "ollama":

        print(
            "[AI Provider] Ollama Streaming -> "
            f"{selected_model}"
        )

        yield from stream_with_ollama(
            message=message,
            system_prompt=final_system_prompt,
            model=selected_model,
        )

        return


    # ==============================================================
    # HUGGING FACE
    # ==============================================================

    if selected_provider == "huggingface":

        raise NotImplementedError(
            "Streaming para Hugging Face ainda "
            "será implementado."
        )


    # ==============================================================
    # PROVEDOR INVÁLIDO
    # ==============================================================

    raise ValueError(
        "Provedor de IA inválido. "
        "Utilize 'ollama' ou 'huggingface'."
    )
