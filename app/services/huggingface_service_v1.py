"""
====================================================================
AI PROVIDER SERVICE
====================================================================

Responsável pela comunicação do DataMind AI Studio com os
provedores de Inteligência Artificial.

Provedores disponíveis:

    1. Ollama
       - Execução local
       - Não utiliza créditos do Hugging Face
       - Ideal para desenvolvimento

    2. Hugging Face
       - Execução através dos Inference Providers
       - Requer HF_TOKEN
       - Pode consumir créditos da conta

A escolha do provedor é feita através da variável:

    AI_PROVIDER

Exemplo:

    AI_PROVIDER=ollama

ou:

    AI_PROVIDER=huggingface

====================================================================
"""

import os

import requests

from huggingface_hub import InferenceClient


# ==================================================================
# CONFIGURAÇÕES
# ==================================================================

# Provedor de IA selecionado.
#
# Por padrão utilizamos Ollama.
AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "ollama",
).lower()


# ==================================================================
# HUGGING FACE
# ==================================================================

HF_TOKEN = os.getenv(
    "HF_TOKEN"
)

HF_MODEL = os.getenv(
    "HF_MODEL",
    "openai/gpt-oss-120b",
)


# ==================================================================
# OLLAMA
# ==================================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
).rstrip("/")


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:4b",
)


# ==================================================================
# CLIENTE HUGGING FACE
# ==================================================================

hf_client = None


if HF_TOKEN:

    hf_client = InferenceClient(
        provider="auto",
        api_key=HF_TOKEN,
    )


# ==================================================================
# SYSTEM PROMPT PADRÃO
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
- Spark
- PostgreSQL
- APIs
- FastAPI
- Hugging Face
- Ollama
- Flet

Regras importantes:

1. Explique conceitos técnicos de forma clara e didática.

2. Quando fornecer código, entregue código completo e funcional.

3. Nunca interrompa um bloco de código no meio.

4. Sempre feche funções, classes, condicionais e estruturas.

5. Utilize boas práticas de programação.

6. Utilize comentários explicativos no código quando forem úteis.

7. Quando o usuário pedir uma alteração em um arquivo,
   apresente o arquivo completo corrigido.

8. Se uma resposta for longa, conclua o conteúdo solicitado.

9. Não invente informações técnicas.

10. Quando houver mais de uma solução possível,
    explique brevemente as alternativas.
"""


# ==================================================================
# OLLAMA
# ==================================================================

def generate_with_ollama(
    message: str,
    system_prompt: str,
) -> str:
    """
    Gera uma resposta utilizando um modelo local do Ollama.

    O Ollama disponibiliza uma API HTTP local.

    Exemplo:

        http://ollama:11434/api/chat

    Parameters
    ----------
    message:
        Pergunta enviada pelo usuário.

    system_prompt:
        Instruções de comportamento do assistente.

    Returns
    -------
    str
        Resposta gerada pelo modelo.
    """

    # --------------------------------------------------------------
    # Endpoint da API do Ollama
    # --------------------------------------------------------------

    url = f"{OLLAMA_URL}/api/chat"


    # --------------------------------------------------------------
    # Corpo da requisição
    # --------------------------------------------------------------

    payload = {

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

        # ----------------------------------------------------------
        # false faz o Ollama retornar a resposta completa
        # em uma única resposta HTTP.
        # ----------------------------------------------------------

        "stream": False,

        # ----------------------------------------------------------
        # Parâmetros de geração
        # ----------------------------------------------------------

        "options": {

            "temperature": 0.7,

            # Número máximo aproximado de tokens gerados.
            "num_predict": 1024,
        },
    }


    # --------------------------------------------------------------
    # Envia requisição
    # --------------------------------------------------------------

    response = requests.post(
        url,
        json=payload,
        timeout=100,
    )


    # --------------------------------------------------------------
    # Verifica erro HTTP
    # --------------------------------------------------------------

    response.raise_for_status()


    # --------------------------------------------------------------
    # Converte resposta para JSON
    # --------------------------------------------------------------

    data = response.json()


    # --------------------------------------------------------------
    # Extrai conteúdo
    # --------------------------------------------------------------

    content = (
        data
        .get("message", {})
        .get("content", "")
    )


    # --------------------------------------------------------------
    # Validação
    # --------------------------------------------------------------

    if not content:

        return (
            "O modelo Ollama não retornou nenhum conteúdo."
        )


    return content


# ==================================================================
# HUGGING FACE
# ==================================================================

def generate_with_huggingface(
    message: str,
    system_prompt: str,
) -> str:
    """
    Gera uma resposta utilizando Hugging Face Inference Providers.
    """

    # --------------------------------------------------------------
    # Verifica token
    # --------------------------------------------------------------

    if not HF_TOKEN:

        raise RuntimeError(
            "HF_TOKEN não foi configurado."
        )


    # --------------------------------------------------------------
    # Verifica cliente
    # --------------------------------------------------------------

    if hf_client is None:

        raise RuntimeError(
            "Cliente Hugging Face não foi inicializado."
        )


    # --------------------------------------------------------------
    # Mensagens
    # --------------------------------------------------------------

    messages = [

        {
            "role": "system",
            "content": system_prompt,
        },

        {
            "role": "user",
            "content": message,
        },
    ]


    # --------------------------------------------------------------
    # Solicitação ao Hugging Face
    # --------------------------------------------------------------

    completion = hf_client.chat.completions.create(

        model=HF_MODEL,

        messages=messages,

        max_tokens=8192,

        temperature=0.7,
    )


    # --------------------------------------------------------------
    # Obtém escolha
    # --------------------------------------------------------------

    choice = completion.choices[0]


    # --------------------------------------------------------------
    # Verifica motivo de finalização.
    #
    # Isso ajuda a diagnosticar respostas cortadas.
    # --------------------------------------------------------------

    finish_reason = getattr(
        choice,
        "finish_reason",
        None,
    )


    print(
        f"[Hugging Face] finish_reason={finish_reason}"
    )


    # --------------------------------------------------------------
    # Conteúdo
    # --------------------------------------------------------------

    content = (
        choice.message.content
        or ""
    )


    if not content:

        return (
            "O modelo Hugging Face não retornou "
            "nenhum conteúdo."
        )


    return content


# ==================================================================
# FUNÇÃO PRINCIPAL
# ==================================================================

def generate_response(
    message: str,
    system_prompt: str | None = None,
) -> str:
    """
    Gera uma resposta utilizando o provedor configurado.

    O provedor é determinado por:

        AI_PROVIDER

    Valores aceitos:

        ollama
        huggingface
    """

    # --------------------------------------------------------------
    # Utiliza o prompt padrão caso nenhum seja fornecido.
    # --------------------------------------------------------------

    final_system_prompt = (
        system_prompt
        if system_prompt
        else DEFAULT_SYSTEM_PROMPT
    )


    # ==============================================================
    # OLLAMA
    # ==============================================================

    if AI_PROVIDER == "ollama":

        print(
            f"[AI Provider] Ollama -> {OLLAMA_MODEL}"
        )

        return generate_with_ollama(
            message=message,
            system_prompt=final_system_prompt,
        )


    # ==============================================================
    # HUGGING FACE
    # ==============================================================

    if AI_PROVIDER == "huggingface":

        print(
            f"[AI Provider] Hugging Face -> {HF_MODEL}"
        )

        return generate_with_huggingface(
            message=message,
            system_prompt=final_system_prompt,
        )


    # ==============================================================
    # PROVEDOR INVÁLIDO
    # ==============================================================

    raise ValueError(
        "AI_PROVIDER inválido. "
        "Utilize 'ollama' ou 'huggingface'."
    )
