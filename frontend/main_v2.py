"""
====================================================================
DATAMIND AI STUDIO - FRONTEND
====================================================================

Interface web desenvolvida com Flet.

Arquitetura:

    Navegador
        |
        v
    Flet Frontend
        |
        v
    FastAPI
        |
        v
    Hugging Face

Funcionalidades:

    - Chat com IA
    - Enter para enviar
    - Shift + Enter para nova linha
    - Histórico da conversa
    - Respostas longas com rolagem
    - Status da API
    - Nova conversa
    - Interface responsiva

====================================================================
"""

import os

import flet as ft
import requests


# ==================================================================
# CONFIGURAÇÕES
# ==================================================================

# Dentro do Docker, "api" é o nome do serviço FastAPI.
# Fora do Docker, podemos utilizar localhost.
API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000",
)


# ==================================================================
# CORES DA INTERFACE
# ==================================================================

BACKGROUND = "#0B0F14"
SIDEBAR_BACKGROUND = "#10151C"
CARD_BACKGROUND = "#151B23"
INPUT_BACKGROUND = "#111720"

TEXT_PRIMARY = "#F1F5F9"
TEXT_SECONDARY = "#CBD5E1"
TEXT_MUTED = "#64748B"

BORDER_COLOR = "#263241"

ACCENT = "#8B5CF6"
ACCENT_HOVER = "#7C3AED"

USER_MESSAGE = "#1E293B"
AI_MESSAGE = "#111827"


# ==================================================================
# FUNÇÃO PRINCIPAL
# ==================================================================

def main(page: ft.Page):
    """
    Cria a interface principal do DataMind AI Studio.
    """

    # ==============================================================
    # CONFIGURAÇÃO DA PÁGINA
    # ==============================================================

    page.title = "DataMind AI Studio"

    page.bgcolor = BACKGROUND

    page.padding = 0

    page.spacing = 0

    page.theme_mode = ft.ThemeMode.DARK


    # ==============================================================
    # HISTÓRICO LOCAL DA CONVERSA
    # ==============================================================

    conversation_history = []


    # ==============================================================
    # FUNÇÕES AUXILIARES
    # ==============================================================

    def create_padding(
        left=0,
        top=0,
        right=0,
        bottom=0,
    ):
        """
        Cria um objeto Padding compatível com a versão atual
        do Flet.
        """

        return ft.Padding(
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )


    # ==============================================================
    # MOSTRAR MENSAGEM NO CHAT
    # ==============================================================

    def create_message(
        text: str,
        is_user: bool = False,
    ):
        """
        Cria um bloco visual para uma mensagem.

        Parameters
        ----------
        text:
            Texto da mensagem.

        is_user:
            True para mensagem do usuário.
            False para mensagem da IA.
        """

        # ----------------------------------------------------------
        # Define o nome do remetente
        # ----------------------------------------------------------

        sender = "Você" if is_user else "DataMind AI"

        # ----------------------------------------------------------
        # Define o ícone
        # ----------------------------------------------------------

        icon = (
            ft.Icons.PERSON_ROUNDED
            if is_user
            else ft.Icons.AUTO_AWESOME_ROUNDED
        )

        # ----------------------------------------------------------
        # Define a cor do ícone
        # ----------------------------------------------------------

        icon_color = (
            TEXT_SECONDARY
            if is_user
            else ACCENT
        )

        # ----------------------------------------------------------
        # Container da mensagem
        # ----------------------------------------------------------

        return ft.Container(
            content=ft.Row(
                [
                    # ------------------------------------------------
                    # ÍCONE
                    # ------------------------------------------------

                    ft.Container(
                        content=ft.Icon(
                            icon,
                            color=icon_color,
                            size=20,
                        ),
                        width=36,
                        height=36,
                        alignment=ft.Alignment.CENTER,
                    ),

                    # ------------------------------------------------
                    # CONTEÚDO
                    # ------------------------------------------------

                    ft.Column(
                        [
                            ft.Text(
                                sender,
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY,
                            ),

                            ft.Container(
                                content=ft.Text(
                                    text,
                                    size=13,
                                    color=TEXT_SECONDARY,
                                    selectable=True,

                                    # Permite que textos grandes
                                    # ocupem várias linhas.
                                    no_wrap=False,
                                ),

                                padding=create_padding(
                                    top=8,
                                    bottom=8,
                                ),
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),

            bgcolor=(
                USER_MESSAGE
                if is_user
                else AI_MESSAGE
            ),

            border_radius=12,

            border=ft.Border(
                left=ft.BorderSide(
                    width=1,
                    color=BORDER_COLOR,
                ),
                top=ft.BorderSide(
                    width=1,
                    color=BORDER_COLOR,
                ),
                right=ft.BorderSide(
                    width=1,
                    color=BORDER_COLOR,
                ),
                bottom=ft.BorderSide(
                    width=1,
                    color=BORDER_COLOR,
                ),
            ),

            padding=14,
        )


    # ==============================================================
    # ÁREA DE MENSAGENS
    # ==============================================================

    chat_messages = ft.Column(
        spacing=18,

        # Permite rolar somente a área das mensagens.
        scroll=ft.ScrollMode.AUTO,

        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )


    # ==============================================================
    # MENSAGEM INICIAL
    # ==============================================================

    welcome_message = ft.Container(
        content=ft.Column(
            [
                ft.Icon(
                    ft.Icons.AUTO_AWESOME_ROUNDED,
                    size=42,
                    color=ACCENT,
                ),

                ft.Text(
                    "Olá! Eu sou o DataMind AI.",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),

                ft.Text(
                    "Posso ajudar com Python, SQL, "
                    "Engenharia de Dados, IA e Agentes de IA.",
                    size=14,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),

        padding=30,

        bgcolor=CARD_BACKGROUND,

        border_radius=16,

        border=ft.Border(
            left=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
            top=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
            right=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
            bottom=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
        ),
    )


    chat_messages.controls.append(
        welcome_message
    )


    # ==============================================================
    # STATUS DA API
    # ==============================================================

    api_status = ft.Row(
        [
            ft.Container(
                width=8,
                height=8,
                bgcolor="#22C55E",
                border_radius=50,
            ),

            ft.Text(
                "API conectada",
                size=11,
                color=TEXT_MUTED,
            ),
        ],
        spacing=6,
    )


    # ==============================================================
    # NOVA CONVERSA
    # ==============================================================

    def new_chat(e=None):
        """
        Limpa a conversa atual.
        """

        conversation_history.clear()

        chat_messages.controls.clear()

        chat_messages.controls.append(
            welcome_message
        )

        page.update()


    # ==============================================================
    # ENVIAR MENSAGEM
    # ==============================================================

    def send_message(e=None):
        """
        Envia a mensagem do usuário para a API.

        O método é utilizado tanto pelo botão quanto
        pelo teclado.
        """

        # ----------------------------------------------------------
        # Obtém o texto digitado
        # ----------------------------------------------------------

        message = message_input.value.strip()

        # ----------------------------------------------------------
        # Não envia mensagens vazias
        # ----------------------------------------------------------

        if not message:
            return

        # ----------------------------------------------------------
        # Adiciona mensagem ao histórico
        # ----------------------------------------------------------

        conversation_history.append(
            {
                "role": "user",
                "content": message,
            }
        )

        # ----------------------------------------------------------
        # Remove mensagem inicial
        # ----------------------------------------------------------

        if welcome_message in chat_messages.controls:
            chat_messages.controls.remove(
                welcome_message
            )

        # ----------------------------------------------------------
        # Adiciona mensagem do usuário
        # ----------------------------------------------------------

        chat_messages.controls.append(
            create_message(
                message,
                is_user=True,
            )
        )

        # ----------------------------------------------------------
        # Limpa o campo
        # ----------------------------------------------------------

        message_input.value = ""

        # ----------------------------------------------------------
        # Desabilita o campo durante a requisição
        # ----------------------------------------------------------

        message_input.disabled = True

        send_button.disabled = True

        page.update()

        # ----------------------------------------------------------
        # Consulta a API
        # ----------------------------------------------------------

        try:

            response = requests.post(
                f"{API_URL}/api/v1/chat",
                json={
                    "message": message,
                },
                timeout=120,
            )

            # ------------------------------------------------------
            # Verifica HTTP
            # ------------------------------------------------------

            response.raise_for_status()

            # ------------------------------------------------------
            # Obtém JSON
            # ------------------------------------------------------

            data = response.json()

            ai_response = data.get(
                "response",
                "A API não retornou uma resposta.",
            )

            # ------------------------------------------------------
            # Salva resposta no histórico
            # ------------------------------------------------------

            conversation_history.append(
                {
                    "role": "assistant",
                    "content": ai_response,
                }
            )

            # ------------------------------------------------------
            # Adiciona resposta da IA
            # ------------------------------------------------------

            chat_messages.controls.append(
                create_message(
                    ai_response,
                    is_user=False,
                )
            )

        except requests.exceptions.Timeout:

            chat_messages.controls.append(
                create_message(
                    "⏱️ A solicitação demorou muito para responder. "
                    "Tente novamente.",
                    is_user=False,
                )
            )

        except requests.exceptions.ConnectionError:

            chat_messages.controls.append(
                create_message(
                    "❌ Não foi possível conectar à API. "
                    "Verifique se o serviço FastAPI está em execução.",
                    is_user=False,
                )
            )

        except requests.exceptions.HTTPError as exc:

            error_message = str(exc)

            try:
                error_data = response.json()

                error_message = error_data.get(
                    "detail",
                    error_message,
                )

            except Exception:
                pass

            chat_messages.controls.append(
                create_message(
                    f"❌ Erro da API:\n\n{error_message}",
                    is_user=False,
                )
            )

        except Exception as exc:

            chat_messages.controls.append(
                create_message(
                    f"❌ Erro inesperado:\n\n{exc}",
                    is_user=False,
                )
            )

        finally:

            # ------------------------------------------------------
            # Reabilita os controles
            # ------------------------------------------------------

            message_input.disabled = False

            send_button.disabled = False

            # ------------------------------------------------------
            # Atualiza a interface
            # ------------------------------------------------------

            page.update()


    # ==============================================================
    # CAMPO DE MENSAGEM
    # ==============================================================

    message_input = ft.TextField(
        hint_text="Digite sua mensagem...",

        # ----------------------------------------------------------
        # Permite múltiplas linhas.
        # ----------------------------------------------------------

        multiline=True,

        min_lines=1,

        max_lines=5,

        expand=True,

        # ----------------------------------------------------------
        # Enter envia a mensagem.
        #
        # No Flet, on_submit é acionado quando o usuário
        # confirma o campo.
        # ----------------------------------------------------------

        on_submit=send_message,

        # ----------------------------------------------------------
        # Aparência
        # ----------------------------------------------------------

        border=ft.InputBorder.NONE,

        text_size=14,

        color=TEXT_PRIMARY,

        hint_style=ft.TextStyle(
            color=TEXT_MUTED,
        ),

        content_padding=ft.Padding(
            left=16,
            right=16,
            top=12,
            bottom=12,
        ),
    )


    # ==============================================================
    # BOTÃO ENVIAR
    # ==============================================================

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,

        tooltip="Enviar mensagem",

        icon_color=ACCENT,

        on_click=send_message,
    )


    # ==============================================================
    # ÁREA DO INPUT
    # ==============================================================

    input_container = ft.Container(
        content=ft.Row(
            [
                message_input,

                send_button,
            ],

            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),

        bgcolor=INPUT_BACKGROUND,

        border_radius=14,

        border=ft.Border(
            left=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
            top=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
            right=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
            bottom=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            ),
        ),

        padding=create_padding(
            left=4,
            right=8,
            top=4,
            bottom=4,
        ),
    )


    # ==============================================================
    # HEADER DO CHAT
    # ==============================================================

    header = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Chat IA",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Text(
                            "Converse com o DataMind AI",
                            size=12,
                            color=TEXT_MUTED,
                        ),
                    ],
                    spacing=2,
                ),

                ft.Container(
                    content=api_status,
                    alignment=ft.Alignment.CENTER_RIGHT,
                    expand=True,
                ),
            ],

            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),

        padding=create_padding(
            left=24,
            right=24,
            top=20,
            bottom=20,
        ),
    )


    # ==============================================================
    # ÁREA DE ROLAGEM DO CHAT
    # ==============================================================

    chat_scroll_area = ft.Container(
        content=chat_messages,

        # Somente essa região ocupa o espaço disponível.
        expand=True,

        padding=create_padding(
            left=24,
            right=24,
            top=10,
            bottom=10,
        ),
    )


    # ==============================================================
    # SIDEBAR
    # ==============================================================

    sidebar = ft.Container(
        content=ft.Column(
            [
                # --------------------------------------------------
                # LOGO
                # --------------------------------------------------

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.AUTO_AWESOME_ROUNDED,
                                color=ACCENT,
                                size=28,
                            ),

                            ft.Text(
                                "DataMind AI",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY,
                            ),
                        ],
                        spacing=10,
                    ),

                    padding=create_padding(
                        left=20,
                        right=20,
                        top=20,
                        bottom=30,
                    ),
                ),

                # --------------------------------------------------
                # NOVA CONVERSA
                # --------------------------------------------------

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ADD_ROUNDED,
                                size=18,
                                color=TEXT_PRIMARY,
                            ),

                            ft.Text(
                                "Nova conversa",
                                size=13,
                                color=TEXT_PRIMARY,
                            ),
                        ],
                        spacing=10,
                    ),

                    bgcolor=CARD_BACKGROUND,

                    border_radius=10,

                    padding=12,

                    margin=create_padding(
                        left=12,
                        right=12,
                        bottom=20,
                    ),

                    on_click=new_chat,
                ),

                # --------------------------------------------------
                # MENU
                # --------------------------------------------------

                ft.Text(
                    "FERRAMENTAS",
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_MUTED,
                ),

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHAT_ROUNDED,
                                size=18,
                                color=ACCENT,
                            ),

                            ft.Text(
                                "Chat IA",
                                size=13,
                                color=TEXT_PRIMARY,
                            ),
                        ],
                        spacing=10,
                    ),

                    padding=12,
                ),

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CODE_ROUNDED,
                                size=18,
                                color=TEXT_MUTED,
                            ),

                            ft.Text(
                                "Python",
                                size=13,
                                color=TEXT_SECONDARY,
                            ),
                        ],
                        spacing=10,
                    ),

                    padding=12,
                ),

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.STORAGE_ROUNDED,
                                size=18,
                                color=TEXT_MUTED,
                            ),

                            ft.Text(
                                "SQL",
                                size=13,
                                color=TEXT_SECONDARY,
                            ),
                        ],
                        spacing=10,
                    ),

                    padding=12,
                ),

                # --------------------------------------------------
                # ESPAÇAMENTO
                # --------------------------------------------------

                ft.Container(
                    expand=True,
                ),

                # --------------------------------------------------
                # HUGGING FACE
                # --------------------------------------------------

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.SMART_TOY_ROUNDED,
                                size=18,
                                color=ACCENT,
                            ),

                            ft.Column(
                                [
                                    ft.Text(
                                        "Hugging Face",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY,
                                    ),

                                    ft.Text(
                                        "Modelo conectado",
                                        size=10,
                                        color=TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                    ),

                    padding=12,

                    bgcolor=CARD_BACKGROUND,

                    border_radius=10,
                ),
            ],

            spacing=4,

            expand=True,
        ),

        width=240,

        bgcolor=SIDEBAR_BACKGROUND,

        border=ft.Border(
            right=ft.BorderSide(
                width=1,
                color=BORDER_COLOR,
            )
        ),
    )


    # ==============================================================
    # ÁREA PRINCIPAL DO CHAT
    # ==============================================================

    chat_area = ft.Column(
        [
            # ------------------------------------------------------
            # HEADER
            # ------------------------------------------------------

            header,

            # ------------------------------------------------------
            # MENSAGENS
            # ------------------------------------------------------

            chat_scroll_area,

            # ------------------------------------------------------
            # INPUT
            # ------------------------------------------------------

            ft.Container(
                content=input_container,

                padding=create_padding(
                    left=24,
                    right=24,
                    top=10,
                    bottom=20,
                ),
            ),
        ],

        spacing=0,

        expand=True,
    )


    # ==============================================================
    # LAYOUT PRINCIPAL
    # ==============================================================

    page.add(
        ft.Row(
            [
                sidebar,

                chat_area,
            ],

            spacing=0,

            expand=True,
        )
    )


# ==================================================================
# INICIALIZAÇÃO COMO APLICAÇÃO ASGI
# ==================================================================

# Exporta a aplicação Flet como ASGI.
#
# O Docker executará:
#
# uvicorn frontend.main:app --host 0.0.0.0 --port 8550
#
# Dessa forma não utilizamos o modo desktop do Flet dentro
# do container Linux.

app = ft.run(
    main,
    export_asgi_app=True,
)
