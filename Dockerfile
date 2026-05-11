# Hugging Face Spaces (Docker SDK) — serves the FastAPI + Plotly dashboard on port 7860
FROM python:3.11-slim-bookworm

WORKDIR /app

# Avoid matplotlib trying to write to a non-writable home dir at import time
ENV MPLCONFIGDIR=/tmp/mpl \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY web/requirements.txt /app/web/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/web/requirements.txt

# Full repo (scripts, gallery PNGs, web package)
COPY . /app

EXPOSE 7860

# HF sets PORT in some runtimes; default to 7860 per Spaces convention
CMD ["/bin/sh", "-c", "exec python -m uvicorn web.app:app --host 0.0.0.0 --port ${PORT:-7860}"]
