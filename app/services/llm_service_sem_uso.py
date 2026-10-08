
"""
Serviço de modelos de linguagem do DataMind AI Studio.

Responsabilidades:
- Selecionar Ollama ou Hugging Face.
- Configurar o cliente de acordo com o provedor.
- Enviar o histórico da conversa ao modelo.
- Retornar o texto gerado.
"""

from typing import Literal

from openai import OpenAI

from app.core.config import settings


Provider = Literal["ollama", "huggingface"]


def get_provider_config(provider: Provider) -> tuple[str, str, str]:
    """
    Retorna a URL, a chave de API e o modelo
    correspondentes ao provedor selecionado.
    """

    if provider == "ollama":
        return (
            settings.ollama_base_url,
            "ollama",
            settings.ollama_model,
        )

    if provider == "huggingface":
        if not settings.hf_token:
            raise ValueError(
                "Configure HF_TOKEN no arquivo .env."
            )

        if not settings.hf_model:
            raise ValueError(
                "Configure HF_MODEL no arquivo .env."
            )

        return (
            settings.hf_base_url,
            settings.hf_token,
            settings.hf_model,
        )

    raise ValueError(
        "Provedor inválido. Use ollama ou huggingface."
    )


def generate_response(
    messages: list[dict[str, str]],
    provider: Provider | None = None,
) -> str:
    """
    Gera uma resposta usando o provedor selecionado.

    Se nenhum provedor for informado, utiliza AI_PROVIDER
    definido nas configurações.
    """

    # Utiliza o padrão da aplicação quando não houver
    # uma seleção explícita na solicitação.
    selected_provider = provider or settings.ai_provider

    if selected_provider not in ("ollama", "huggingface"):
        raise ValueError(
            "Provedor inválido. Use ollama ou huggingface."
        )

    # Recupera as configurações específicas do provedor.
    base_url, api_key, model = get_provider_config(
        selected_provider
    )

    # Ambos os endpoints oferecem compatibilidade com
    # o formato de chat completions utilizado pelo SDK.
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=180.0,
    )

    # Envia as mensagens da conversa ao modelo.
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=settings.ai_temperature,
        max_tokens=settings.ai_max_tokens,
        stream=False,
    )

    # Extrai o texto da resposta.
    content = completion.choices[0].message.content

    if not content:
        raise ValueError(
            "O modelo retornou uma resposta vazia."
        )

    return content