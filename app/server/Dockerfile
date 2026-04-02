FROM python:3.12-slim

LABEL maintainer="Heng Rathpisey"
LABEL description="ITC-OS 2026 Presence Server — tracks Linux users via who/last"

# who/last need these utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends procps && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# Health check: hit /api/health every 30s
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

ENTRYPOINT ["python3", "app.py"]
CMD ["--host", "0.0.0.0", "--port", "5000"]
