"""
====================================================================
HUGGING FACE SERVICE
====================================================================

Responsável pela comunicação do DataMind AI Studio
com o Hugging Face Inference Providers.

Responsabilidades:

    - Autenticar no Hugging Face.
    - Selecionar o modelo.
    - Enviar mensagens para o modelo.
    - Retornar a resposta gerada.

O modelo pode ser informado individualmente em cada requisição.

Caso nenhum modelo seja informado, será utilizado:

    HF_MODEL

====================================================================
"""

import os

from huggingface_hub import InferenceClient


# ==================================================================
# CONFIGURAÇÕES
# ==================================================================

# Token da API do Hugging Face.
#
# Deve ser configurado através da variável:
#
#     HF_TOKEN
#
# Não coloque o token diretamente neste arquivo.
#
HF_TOKEN = os.getenv(
    "HF_TOKEN",
)


# Modelo padrão do Hugging Face.
#
# Pode ser substituído por outro modelo através
# da variável de ambiente HF_MODEL.
#
HF_MODEL = os.getenv(
    "HF_MODEL",
    "openai/gpt-oss-120b",
)


# ==================================================================
# CLIENTE HUGGING FACE
# ==================================================================

# O cliente somente é criado quando existe um token.
#
# Isso permite que a aplicação seja inicializada mesmo
# quando o Hugging Face não estiver configurado.
#
hf_client = None


if HF_TOKEN:

    hf_client = InferenceClient(
        provider="auto",
        api_key=HF_TOKEN,
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

2. Quando fornecer código, entregue código completo e funcional.

3. Nunca interrompa um bloco de código.

4. Sempre feche funções, classes, condicionais e estruturas.

5. Utilize boas práticas de programação.

6. Utilize comentários explicativos no código quando forem úteis.

7. Quando o usuário pedir uma alteração em um arquivo,
   apresente o arquivo completo corrigido.

8. Se uma resposta for longa, conclua o conteúdo solicitado.

9. Não invente informações técnicas.

10. Quando houver mais de uma solução possível,
    explique brevemente as alternativas.

11. Priorize exemplos práticos.
"""


# ==================================================================
# GERAÇÃO DE RESPOSTA
# ==================================================================

def generate_with_huggingface(
    message: str,
    system_prompt: str,
    model: str | None = None,
) -> str:
    """
    Gera uma resposta utilizando o Hugging Face.

    Parameters
    ----------
    message:
        Pergunta enviada pelo usuário.

    system_prompt:
        Prompt de sistema utilizado pelo assistente.

    model:
        Modelo Hugging Face escolhido.

        Quando None, utiliza HF_MODEL.

    Returns
    -------
    str
        Resposta completa gerada pelo modelo.

    Raises
    ------
    RuntimeError
        Quando o token não foi configurado ou
        o cliente não foi inicializado.
    """

    # --------------------------------------------------------------
    # Verifica token.
    # --------------------------------------------------------------

    if not HF_TOKEN:

        raise RuntimeError(
            "HF_TOKEN não foi configurado. "
            "Configure o token do Hugging Face "
            "nas variáveis de ambiente."
        )


    # --------------------------------------------------------------
    # Verifica cliente.
    # --------------------------------------------------------------

    if hf_client is None:

        raise RuntimeError(
            "Cliente Hugging Face não foi inicializado."
        )


    # --------------------------------------------------------------
    # Define o modelo.
    # --------------------------------------------------------------

    selected_model = (
        model
        if model
        else HF_MODEL
    )


    # --------------------------------------------------------------
    # Exibe informação no log.
    # --------------------------------------------------------------

    print(
        "[Hugging Face] Modelo: "
        f"{selected_model}"
    )


    # --------------------------------------------------------------
    # Monta as mensagens.
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
    # Chama o modelo.
    # --------------------------------------------------------------

    try:

        completion = (
            hf_client.chat.completions.create(

                model=selected_model,

                messages=messages,

                max_tokens=8192,

                temperature=0.7,
            )
        )

    except Exception as exc:

        raise RuntimeError(
            "Erro ao consultar o Hugging Face: "
            f"{exc}"
        ) from exc


    # --------------------------------------------------------------
    # Verifica se houve alguma escolha.
    # --------------------------------------------------------------

    if not completion.choices:

        raise RuntimeError(
            "O Hugging Face não retornou nenhuma escolha."
        )


    # --------------------------------------------------------------
    # Obtém a primeira escolha.
    # --------------------------------------------------------------

    choice = completion.choices[0]


    # --------------------------------------------------------------
    # Motivo de finalização.
    #
    # Essa informação é útil para diagnosticar respostas
    # que eventualmente tenham sido interrompidas pelo limite
    # de tokens.
    # --------------------------------------------------------------

    finish_reason = getattr(
        choice,
        "finish_reason",
        None,
    )


    print(
        "[Hugging Face] "
        f"finish_reason={finish_reason}"
    )


    # --------------------------------------------------------------
    # Extrai conteúdo.
    # --------------------------------------------------------------

    content = (
        choice.message.content
        or ""
    )


    # --------------------------------------------------------------
    # Validação.
    # --------------------------------------------------------------

    if not content:

        raise RuntimeError(
            "O modelo Hugging Face não retornou conteúdo."
        )


    return content.strip()
