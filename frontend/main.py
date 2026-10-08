"""
====================================================================
DATAMIND AI STUDIO - FRONTEND
====================================================================

Frontend da plataforma DataMind AI Studio.

Arquitetura:

    Navegador
        |
        v
    Flet
        |
        v
    FastAPI
        |
        +--------------------+
        |                    |
        v                    v
     Ollama            Hugging Face

O frontend é executado dentro do Docker.

A API é acessada através de:

    http://api:8000

O navegador acessa o Flet através de:

    http://localhost:8550
====================================================================
"""

# ====================================================================
# IMPORTAÇÕES
# ====================================================================

import os
import requests
import flet as ft


# ====================================================================
# CONFIGURAÇÕES
# ====================================================================

# URL da API FastAPI.
#
# Dentro do Docker, "api" é o nome do serviço no docker-compose.
API_URL = os.getenv(
    "API_URL",
    "http://api:8000",
).rstrip("/")


# Nome da aplicação.
APP_NAME = os.getenv(
    "APP_NAME",
    "DataMind AI Studio",
)


# ====================================================================
# CONFIGURAÇÃO DOS MODELOS
# ====================================================================

# Modelos disponíveis no Ollama.
OLLAMA_MODELS = [
    "qwen2.5-coder:3b",
]


# Modelos disponíveis no Hugging Face.
#
# Você poderá adicionar outros modelos posteriormente.
HUGGINGFACE_MODELS = [
    "openai/gpt-oss-120b",
]


# ====================================================================
# FUNÇÃO PRINCIPAL
# ====================================================================

def main(page: ft.Page):
    """
    Cria a interface principal do DataMind AI Studio.
    """

    # ---------------------------------------------------------------
    # CONFIGURAÇÕES DA PÁGINA
    # ---------------------------------------------------------------

    page.title = APP_NAME

    page.theme_mode = ft.ThemeMode.DARK

    page.padding = 0

    page.bgcolor = "#0f172a"


    # ---------------------------------------------------------------
    # ESTADO DA APLICAÇÃO
    # ---------------------------------------------------------------

    # Provedor atualmente selecionado.
    selected_provider = "ollama"

    # Modelo atualmente selecionado.
    selected_model = OLLAMA_MODELS[0]


    # ---------------------------------------------------------------
    # ÁREA DE MENSAGENS
    # ---------------------------------------------------------------

    messages_column = ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        auto_scroll=True,
    )


    # ================================================================
    # FUNÇÕES DE INTERFACE
    # ================================================================

    def add_user_message(message: str):
        """
        Adiciona a mensagem do usuário ao histórico visual.
        """

        message_text = ft.Text(
            message,
            selectable=True,
            size=14,
            color="#f8fafc",
            no_wrap=False,
        )

        bubble = ft.Container(
            content=message_text,
            padding=15,
            bgcolor="#1e3a5f",
            border_radius=12,
            width=700,
        )

        messages_column.controls.append(
            ft.Row(
                [bubble],
                alignment=ft.MainAxisAlignment.END,
            )
        )


    def create_ai_message():
        """
        Cria o componente que exibirá a resposta da IA.

        Utilizamos Markdown para permitir:

        - parágrafos
        - listas
        - código
        - títulos
        - negrito
        - tabelas
        """

        response_markdown = ft.Markdown(
            value="",
            selectable=True,
        )

        bubble = ft.Container(
            content=response_markdown,
            padding=15,
            bgcolor="#1e293b",
            border_radius=12,
            width=800,
        )

        messages_column.controls.append(
            ft.Row(
                [bubble],
                alignment=ft.MainAxisAlignment.START,
            )
        )

        return response_markdown


    # ================================================================
    # ENVIO DA MENSAGEM
    # ================================================================

    def send_message(e=None):
        """
        Envia a mensagem do usuário para a API FastAPI.
        """

        message = message_input.value.strip()

        if not message:
            return


        # ------------------------------------------------------------
        # Adiciona mensagem do usuário.
        # ------------------------------------------------------------

        add_user_message(message)


        # ------------------------------------------------------------
        # Limpa o campo de entrada.
        # ------------------------------------------------------------

        message_input.value = ""


        # ------------------------------------------------------------
        # Cria o componente da resposta da IA.
        # ------------------------------------------------------------

        ai_response = create_ai_message()


        # Atualiza a interface.
        page.update()


        # ------------------------------------------------------------
        # Monta o payload.
        # ------------------------------------------------------------

        payload = {
            "provider": selected_provider,
            "model": selected_model,
            "message": message,
        }


        try:

            # --------------------------------------------------------
            # Chamada para a API FastAPI.
            # --------------------------------------------------------

            response = requests.post(
                f"{API_URL}/api/v1/chat/stream",
                json=payload,
                stream=True,
                timeout=300,
            )


            # Verifica HTTP 4xx/5xx.
            response.raise_for_status()


            # --------------------------------------------------------
            # Recebe a resposta em streaming.
            # --------------------------------------------------------

            complete_response = ""


            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True,
            ):

                if not chunk:
                    continue


                # Adiciona o pedaço recebido.
                complete_response += chunk


                # Atualiza o Markdown.
                ai_response.value = complete_response


                # Atualiza a interface.
                page.update()


        except requests.exceptions.RequestException as exc:

            ai_response.value = (
                "### Erro de comunicação com a API\n\n"
                f"```text\n{exc}\n```"
            )

            page.update()


        except Exception as exc:

            ai_response.value = (
                "### Erro inesperado\n\n"
                f"```text\n{exc}\n```"
            )

            page.update()


    # ================================================================
    # SELEÇÃO DO PROVEDOR
    # ================================================================

    def provider_changed(e):
        """
        Atualiza o provedor e os modelos disponíveis.
        """

        nonlocal selected_provider
        nonlocal selected_model


        selected_provider = e.control.value


        # ------------------------------------------------------------
        # Ollama
        # ------------------------------------------------------------

        if selected_provider == "ollama":

            model_dropdown.options = [
                ft.DropdownOption(
                    key=model,
                    text=model,
                )
                for model in OLLAMA_MODELS
            ]

            selected_model = OLLAMA_MODELS[0]


        # ------------------------------------------------------------
        # Hugging Face
        # ------------------------------------------------------------

        else:

            model_dropdown.options = [
                ft.DropdownOption(
                    key=model,
                    text=model,
                )
                for model in HUGGINGFACE_MODELS
            ]

            selected_model = HUGGINGFACE_MODELS[0]


        model_dropdown.value = selected_model

        page.update()


    def model_changed(e):
        """
        Atualiza o modelo selecionado.
        """

        nonlocal selected_model

        selected_model = e.control.value

        page.update()


    # ================================================================
    # COMPONENTE - PROVIDER
    # ================================================================

    provider_dropdown = ft.Dropdown(
        label="Provedor de IA",
        value="ollama",
        options=[
            ft.DropdownOption(
                key="ollama",
                text="Ollama",
            ),
            ft.DropdownOption(
                key="huggingface",
                text="Hugging Face",
            ),
        ],
        on_select=provider_changed,
        width=220,
    )


    # ================================================================
    # COMPONENTE - MODEL
    # ================================================================

    model_dropdown = ft.Dropdown(
        label="Modelo",
        value=selected_model,
        options=[
            ft.DropdownOption(
                key=model,
                text=model,
            )
            for model in OLLAMA_MODELS
        ],
        on_select=model_changed,
        width=300,
    )


    # ================================================================
    # CAMPO DE MENSAGEM
    # ================================================================

    message_input = ft.TextField(
        hint_text="Digite sua pergunta...",
        multiline=True,
        min_lines=1,
        max_lines=8,
        expand=True,
        border_radius=12,
        border_color="#334155",
        focused_border_color="#3b82f6",
        bgcolor="#1e293b",
        color="#f8fafc",
        text_size=14,

        # Enter envia a mensagem.
        # Shift + Enter permite nova linha.
        on_submit=send_message,
    )


    # ================================================================
    # BOTÃO ENVIAR
    # ================================================================

    send_button = ft.IconButton(
        icon=ft.Icons.SEND,
        tooltip="Enviar",
        on_click=send_message,
    )


    # ================================================================
    # CABEÇALHO
    # ================================================================

    header = ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    "DataMind AI Studio",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#f8fafc",
                ),

                ft.Container(
                    expand=True,
                ),

                provider_dropdown,

                model_dropdown,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),

        padding=15,

        bgcolor="#111827",
    )


    # ================================================================
    # ÁREA DE ENTRADA
    # ================================================================

    input_area = ft.Container(
        content=ft.Row(
            [
                message_input,
                send_button,
            ],
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),

        padding=15,

        bgcolor="#111827",
    )


    # ================================================================
    # LAYOUT PRINCIPAL
    # ================================================================

    page.add(
        ft.Column(
            [
                header,

                ft.Container(
                    content=messages_column,
                    expand=True,
                    padding=20,
                ),

                input_area,
            ],
            expand=True,
            spacing=0,
        )
    )


# ====================================================================
# EXPORTAÇÃO ASGI
# ====================================================================

# IMPORTANTE:
#
# O Docker executará:
#
#     uvicorn app.frontend.main:app
#
# Portanto precisamos disponibilizar uma variável global chamada "app".
#
# O parâmetro export_asgi_app=True transforma o aplicativo Flet
# em uma aplicação ASGI que pode ser executada pelo Uvicorn.

app = ft.run(
    main,
    export_asgi_app=True,
)
