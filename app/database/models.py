"""
Modelos iniciais do banco de dados.

Nesta fase, criamos estruturas para:
- Projetos
- Conversas
- Mensagens
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Project(Base):
    """
    Representa um projeto criado pelo usuário.
    """

    __tablename__ = "projects"

    # Identificador único do projeto.
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Nome do projeto.
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # Descrição opcional.
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Data de criação gerada pelo PostgreSQL.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relacionamento com as conversas do projeto.
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class Conversation(Base):
    """
    Representa uma conversa armazenada na plataforma.
    """

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Projeto associado. Pode ser nulo para conversas independentes.
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
    )

    # Título exibido no histórico.
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="Nova conversa",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relacionamento com o projeto.
    project: Mapped[Project | None] = relationship(
        back_populates="conversations",
    )

    # Mensagens ordenadas pelo identificador.
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.id",
    )


class Message(Base):
    """
    Armazena uma mensagem do usuário ou do assistente.
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Identifica a conversa à qual a mensagem pertence.
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Papel da mensagem: user, assistant ou system.
    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # Conteúdo textual da mensagem.
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relacionamento com a conversa.
    conversation: Mapped[Conversation] = relationship(
        back_populates="messages",
    )