
"""
====================================================================
DATAMIND AI STUDIO - FRONTEND
====================================================================

Interface web desenvolvida com Flet.

Funcionalidades:
1. Exibir o painel inicial.
2. Verificar a conexão com a API.
3. Enviar perguntas para o endpoint /api/v1/chat.
4. Exibir as respostas geradas pelo Hugging Face.

A aplicação é executada como ASGI pelo Uvicorn.
====================================================================
"""

import os

import flet as ft
import requests


# ------------------------------------------------------------------
# CONFIGURAÇÃO
# ------------------------------------------------------------------

# URL interna da API na rede Docker.
API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000",
)


def main(page: ft.Page):
    """
    Monta a interface do DataMind AI Studio.
    """

    # ==============================================================
    # CONFIGURAÇÕES DA PÁGINA
    # ==============================================================

    page.title = "DataMind AI Studio"
    page.padding = 24
    page.theme_mode = ft.ThemeMode.LIGHT

    # ==============================================================
    # COMPONENTES
    # ==============================================================

    status_text = ft.Text(
        "API: ainda não consultada",
    )

    # Campo em que o usuário digitará sua pergunta.
    message_input = ft.TextField(
        label="Digite sua pergunta",
        hint_text="Ex.: Explique o que é Apache Kafka",
        multiline=True,
        min_lines=2,
        max_lines=5,
        expand=True,
    )

    # Área que exibirá a resposta do modelo.
    response_text = ft.Text(
        "Olá! Sou o assistente do DataMind AI Studio. "
        "Digite uma pergunta para começar.",
        selectable=True,
    )

    # ==============================================================
    # VERIFICAR A API
    # ==============================================================

    def check_api(_):
        """
        Consulta o health check do backend.
        """

        try:
            response = requests.get(
                f"{API_URL}/api/v1/health",
                timeout=10,
            )

            response.raise_for_status()
            data = response.json()

            status_text.value = (
                f"API: {data['status']} — "
                f"versão {data['version']}"
            )

        except requests.RequestException as exc:
            status_text.value = (
                f"Falha ao consultar a API: {exc}"
            )

        except (KeyError, ValueError):
            status_text.value = (
                "A API respondeu, mas o formato da resposta "
                "não era o esperado."
            )

        page.update()

    # ==============================================================
    # ENVIAR PERGUNTA AO CHAT
    # ==============================================================

    def send_message(_):
        """
        Envia a pergunta para o FastAPI e apresenta a resposta.
        """

        # Remove espaços desnecessários no início e no fim.
        message = (message_input.value or "").strip()

        # Impede o envio de uma mensagem vazia.
        if not message:
            response_text.value = (
                "Digite uma pergunta antes de enviar."
            )
            page.update()
            return

        # Informa ao usuário que a solicitação está sendo processada.
        response_text.value = "Consultando o modelo de IA..."
        send_button.disabled = True
        page.update()

        try:
            # Envia a pergunta para o endpoint do Chat.
            response = requests.post(
                f"{API_URL}/api/v1/chat",
                json={
                    "message": message,
                },
                timeout=120,
            )

            # Verifica se o backend retornou erro HTTP.
            response.raise_for_status()

            # Converte o JSON recebido.
            data = response.json()

            # Exibe a resposta gerada pelo modelo.
            response_text.value = data.get(
                "response",
                "A API não retornou o campo 'response'.",
            )

            # Limpa o campo após o envio bem-sucedido.
            message_input.value = ""

        except requests.Timeout:
            response_text.value = (
                "A solicitação demorou mais que o esperado. "
                "Tente novamente em alguns instantes."
            )

        except requests.HTTPError as exc:
            # Tenta mostrar a mensagem de erro enviada pela API.
            try:
                error_data = exc.response.json()
                detail = error_data.get(
                    "detail",
                    str(exc),
                )
            except (ValueError, AttributeError):
                detail = str(exc)

            response_text.value = (
                f"Erro retornado pela API: {detail}"
            )

        except requests.RequestException as exc:
            response_text.value = (
                f"Não foi possível acessar a API: {exc}"
            )

        except (ValueError, AttributeError):
            response_text.value = (
                "Não foi possível interpretar a resposta da API."
            )

        finally:
            # Reabilita o botão após a solicitação.
            send_button.disabled = False
            page.update()

    # ==============================================================
    # BOTÕES
    # ==============================================================

    send_button = ft.ElevatedButton(
        "Enviar pergunta",
        on_click=send_message,
    )

    check_button = ft.ElevatedButton(
        "Verificar conexão com a API",
        on_click=check_api,
    )

    # ==============================================================
    # MONTAGEM DA INTERFACE
    # ==============================================================

    page.add(
        ft.Column(
            controls=[
                # Cabeçalho.
                ft.Text(
                    "DataMind AI Studio",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Ambiente de desenvolvimento de IA, "
                    "Agentes de IA e Engenharia de Dados."
                ),

                ft.Divider(),

                # Status da API.
                ft.Text(
                    "Painel de conexão",
                    size=22,
                    weight=ft.FontWeight.W_500,
                ),

                status_text,
                check_button,

                ft.Divider(),

                # Área do Chat.
                ft.Text(
                    "Chat com Inteligência Artificial",
                    size=22,
                    weight=ft.FontWeight.W_500,
                ),

                message_input,
                send_button,

                # Área para exibir a resposta.
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Resposta do assistente",
                                weight=ft.FontWeight.BOLD,
                            ),
                            response_text,
                        ],
                        spacing=12,
                    ),
                    padding=16,
                    border_radius=10,
                ),
            ],
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
    )


# ==============================================================
# EXPORTAÇÃO ASGI
# ==============================================================

# O Uvicorn executará esta aplicação web na porta 8550.
app = ft.run(
    main,
    export_asgi_app=True,
)