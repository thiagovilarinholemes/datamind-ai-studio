"""
Configuração da conexão com o PostgreSQL usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """
    Classe base dos modelos ORM.

    Todos os modelos de tabelas herdarão desta classe.
    """
    pass


# Cria o mecanismo de conexão com o banco.
# pool_pre_ping ajuda a identificar conexões inválidas.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


# Fábrica de sessões para interagir com o banco.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    """
    Fornece uma sessão do banco para os endpoints.

    O bloco finally garante o fechamento da sessão,
    inclusive quando ocorre uma exceção.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()