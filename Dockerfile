FROM python:3.12-alpine
ENV ENV=PROD
ENV PYTHONUNBUFFERED=1 \
    SENTRY_ENVIRONMENT=${ENV} \
    PATH="/root/.local/bin:${PATH}"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
ADD https://install.python-poetry.org install-poetry.py
RUN python install-poetry.py \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --no-cache --only main \
    && rm -f pyproject.toml poetry.lock install-poetry.py
COPY /src .
RUN adduser -D -u 1000 -s /sbin/nologin bot \
    && chown -R bot:bot /app
USER bot
ENTRYPOINT ["python", "main.py"]
