FROM python:3.12-alpine
ENV ENV=PROD
ENV PYTHONUNBUFFERED=1 \
    SENTRY_ENVIRONMENT=${ENV}
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
COPY /src pyproject.toml uv.lock ./
RUN uv sync \
    --frozen \
    --no-dev \
    --compile-bytecode \
    --python-preference only-system \
    && rm -f pyproject.toml uv.lock
RUN adduser -D -u 1000 -s /sbin/nologin bot \
    && chown -R bot:bot /app
USER bot
ENTRYPOINT ["uv", "run", "main.py"]
