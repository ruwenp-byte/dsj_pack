FROM python:3.11-slim


ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc wget curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# COPY app.py /app/app.py
COPY . /app/

# Optional schnelle Sanity-Checks (nicht zwingend)
RUN python -c "import fastapi, uvicorn, mlflow"

EXPOSE 8000
# ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]