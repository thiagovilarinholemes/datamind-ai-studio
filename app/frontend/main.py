"""
====================================================================
DATAMIND AI STUDIO - FRONTEND
====================================================================

Frontend da plataforma DataMind AI Studio.

Arquitetura:

    Navegador
        |
        v
    Flet :8550
        |
        v
    FastAPI :8000
        |
        +--------------------+
        |                    |
        v                    v
     Ollama            Hugging Face

Funcionalidades:

    - Chat com IA
    - Streaming das respostas
    - Seleção do provedor
    - Seleção dinâmica do modelo
    - Markdown nas respostas
    - Histórico da conversa durante a sessão
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

# URL da API.

# Dentro do Docker:
#
#     http://api:8000
#
# O navegador NÃO utiliza essa URL diretamente.
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
# FUNÇÃO PRINCIPAL
# ====================================================================

def main(page: ft.Page):
    """
    Cria a interface principal do DataMind AI Studio.
    """

    # ================================================================
    # CONFIGURAÇÕES DA PÁGINA
    # ================================================================

    page.title = APP_NAME

    page.theme_mode = ft.ThemeMode.DARK

    page.padding = 0

    page.bgcolor = "#0f172a"


    # ================================================================
    # ESTADO DA APLICAÇÃO
    # ================================================================

    # Provedor selecionado.
    selected_provider = "ollama"

    # Modelo selecionado.
    selected_model = ""


    # ================================================================
    # MODELOS
    # ================================================================

    ollama_models = []

    huggingface_models = []


    # ================================================================
    # ÁREA DE MENSAGENS
    # ================================================================

    messages_column = ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        auto_scroll=True,
    )


    # ================================================================
    # COMPONENTES
    # ================================================================

    provider_dropdown = ft.Dropdown(
        label="Provedor de IA",
        value="ollama",
        options=[],
        width=220,
    )


    model_dropdown = ft.Dropdown(
        label="Modelo",
        value=None,
        options=[],
        width=320,
    )


    status_text = ft.Text(
        "Carregando modelos...",
        size=12,
        color="#94a3b8",
    )


    # ================================================================
    # FUNÇÃO PARA CRIAR AS OPÇÕES
    # ================================================================

    def create_model_options(models: list[str]):
        """
        Converte uma lista de nomes de modelos em DropdownOption.
        """

        return [
            ft.DropdownOption(
                key=model,
                text=model,
            )
            for model in models
        ]


    # ================================================================
    # CARREGAR MODELOS
    # ================================================================

    def load_models():
        """
        Consulta a API e carrega os modelos disponíveis.
        """

        nonlocal ollama_models
        nonlocal huggingface_models
        nonlocal selected_model


        # ------------------------------------------------------------
        # Ollama
        # ------------------------------------------------------------

        try:

            response = requests.get(
                f"{API_URL}/api/v1/models/ollama",
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            ollama_models = data.get(
                "models",
                [],
            )

        except Exception as exc:

            print(
                f"[Frontend] Erro ao carregar modelos Ollama: {exc}"
            )

            ollama_models = []


        # ------------------------------------------------------------
        # Hugging Face
        # ------------------------------------------------------------

        try:

            response = requests.get(
                f"{API_URL}/api/v1/models/huggingface",
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            huggingface_models = data.get(
                "models",
                [],
            )

        except Exception as exc:

            print(
                "[Frontend] Erro ao carregar modelos "
                f"Hugging Face: {exc}"
            )

            huggingface_models = []


        # ------------------------------------------------------------
        # Atualiza o dropdown de provedores.
        # ------------------------------------------------------------

        provider_dropdown.options = [
            ft.DropdownOption(
                key="ollama",
                text="Ollama",
            ),
            ft.DropdownOption(
                key="huggingface",
                text="Hugging Face",
            ),
        ]


        # ------------------------------------------------------------
        # Seleciona os modelos do Ollama.
        # ------------------------------------------------------------

        if ollama_models:

            model_dropdown.options = create_model_options(
                ollama_models
            )

            selected_model = ollama_models[0]

            model_dropdown.value = selected_model

            status_text.value = (
                f"Ollama: {len(ollama_models)} modelo(s) disponível(is)"
            )

        else:

            model_dropdown.options = []

            model_dropdown.value = None

            selected_model = ""

            status_text.value = (
                "Nenhum modelo Ollama disponível."
            )


        page.update()


    # ================================================================
    # TROCA DE PROVEDOR
    # ================================================================

    def provider_changed(e):
        """
        Atualiza os modelos quando o usuário troca o provedor.
        """

        nonlocal selected_provider
        nonlocal selected_model


        selected_provider = e.control.value


        # ------------------------------------------------------------
        # Ollama
        # ------------------------------------------------------------

        if selected_provider == "ollama":

            models = ollama_models

            status_text.value = (
                f"Ollama: {len(models)} modelo(s) disponível(is)"
            )


        # ------------------------------------------------------------
        # Hugging Face
        # ------------------------------------------------------------

        else:

            models = huggingface_models

            status_text.value = (
                "Hugging Face: "
                f"{len(models)} modelo(s) configurado(s)"
            )


        # ------------------------------------------------------------
        # Atualiza modelos.
        # ------------------------------------------------------------

        model_dropdown.options = create_model_options(
            models
        )


        # ------------------------------------------------------------
        # Seleciona o primeiro modelo.
        # ------------------------------------------------------------

        if models:

            selected_model = models[0]

            model_dropdown.value = selected_model

        else:

            selected_model = ""

            model_dropdown.value = None


        page.update()


    # ================================================================
    # TROCA DE MODELO
    # ================================================================

    def model_changed(e):
        """
        Atualiza o modelo selecionado.
        """

        nonlocal selected_model

        selected_model = e.control.value

        print(
            f"[Frontend] Modelo selecionado: {selected_model}"
        )

        page.update()


    # ================================================================
    # EVENTOS DOS DROPDOWNS
    # ================================================================

    provider_dropdown.on_select = provider_changed

    model_dropdown.on_select = model_changed


    # ================================================================
    # ADICIONAR MENSAGEM DO USUÁRIO
    # ================================================================

    def add_user_message(message: str):
        """
        Adiciona a mensagem do usuário ao histórico.
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


    # ================================================================
    # CRIAR RESPOSTA DA IA
    # ================================================================

    def create_ai_message():
        """
        Cria o componente visual da resposta da IA.

        Markdown permite:

            - títulos
            - listas
            - código
            - tabelas
            - negrito
            - parágrafos
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
    # ENVIAR MENSAGEM
    # ================================================================

    def send_message(e=None):
        """
        Envia a mensagem para o endpoint de streaming.
        """

        message = message_input.value.strip()


        if not message:
            return


        # ------------------------------------------------------------
        # Verifica se existe um modelo.
        # ------------------------------------------------------------

        if not selected_model:

            ai_response = create_ai_message()

            ai_response.value = (
                "### Nenhum modelo disponível\n\n"
                "Verifique se o provedor de IA está disponível."
            )

            page.update()

            return


        # ------------------------------------------------------------
        # Adiciona mensagem do usuário.
        # ------------------------------------------------------------

        add_user_message(message)


        # ------------------------------------------------------------
        # Limpa o campo.
        # ------------------------------------------------------------

        message_input.value = ""


        # ------------------------------------------------------------
        # Cria resposta da IA.
        # ------------------------------------------------------------

        ai_response = create_ai_message()


        page.update()


        # ============================================================
        # PAYLOAD
        # ============================================================

        payload = {
            "provider": selected_provider,
            "model": selected_model,
            "message": message,
        }


        print(
            "[Frontend] Enviando para IA:"
        )

        print(
            f"Provider: {selected_provider}"
        )

        print(
            f"Model: {selected_model}"
        )


        # ============================================================
        # REQUEST
        # ============================================================

        try:

            response = requests.post(
                f"{API_URL}/api/v1/chat/stream",
                json=payload,
                stream=True,
                timeout=300,
            )


            response.raise_for_status()


            # --------------------------------------------------------
            # Streaming
            # --------------------------------------------------------

            complete_response = ""


            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True,
            ):

                if not chunk:
                    continue


                complete_response += chunk


                ai_response.value = complete_response


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
        content=ft.Column(
            [
                status_text,

                ft.Row(
                    [
                        message_input,
                        send_button,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
        ),

        padding=15,

        bgcolor="#111827",
    )


    # ================================================================
    # LAYOUT
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


    # ================================================================
    # CARREGA OS MODELOS
    # ================================================================

    load_models()


# ====================================================================
# EXPORTAÇÃO ASGI
# ====================================================================

# O Docker executa:
#
#     uvicorn app.frontend.main:app
#
# Portanto precisamos disponibilizar "app".

app = ft.run(
    main,
    export_asgi_app=True,
)
