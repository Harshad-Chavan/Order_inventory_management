# -------------------------------
# Base image
# -------------------------------
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

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
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh","./entrypoint.sh"]