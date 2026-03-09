FROM python:3.11-slim-bookworm

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir .

ENTRYPOINT ["rockfish-mcp"]
