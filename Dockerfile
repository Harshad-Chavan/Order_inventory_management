# -------------------------------
# Base image
# -------------------------------
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m appuser
USER appuser

WORKDIR /app

# -------------------------------
# Install uv
# -------------------------------
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# -------------------------------
# Dependencies layer
# -------------------------------
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

# -------------------------------
# Application layer
# -------------------------------
COPY . ./app

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["uv","run","uvicorn"]

CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]
