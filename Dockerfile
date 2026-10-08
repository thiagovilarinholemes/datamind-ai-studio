FROM python:3.12-slim


# ------------------------------------------------
# Configurações do Python
# ------------------------------------------------

# Não cria arquivos .pyc.
ENV PYTHONDONTWRITEBYTECODE=1

# Mostra os logs imediatamente no Docker.
ENV PYTHONUNBUFFERED=1


# ------------------------------------------------
# Diretório de trabalho
# ------------------------------------------------

WORKDIR /workspace


# ------------------------------------------------
# Dependências
# ------------------------------------------------

# Copia primeiro o requirements.txt para aproveitar
# o cache das camadas do Docker.

COPY requirements.txt .


# ------------------------------------------------
# Instala as dependências
# ------------------------------------------------

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ------------------------------------------------
# Código da aplicação
# ------------------------------------------------

# Copia todo o pacote principal.
#
# Isso inclui:
#
# app/
# ├── main.py
# ├── api/
# ├── models/
# ├── services/
# └── frontend/
#     └── main.py
#
COPY app ./app


# ------------------------------------------------
# Testes
# ------------------------------------------------

COPY tests ./tests


# ------------------------------------------------
# Documentação
# ------------------------------------------------

COPY README.md .


# ------------------------------------------------
# Porta padrão da API
# ------------------------------------------------

EXPOSE 8000


# ------------------------------------------------
# Comando padrão
# ------------------------------------------------
#
# IMPORTANTE:
# O CMD precisa estar em uma única instrução válida.
#
# O docker-compose pode sobrescrever esse comando
# quando for iniciar o frontend.
# ------------------------------------------------

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
