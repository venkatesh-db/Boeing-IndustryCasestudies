FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agentkit ./agentkit
COPY app ./app
COPY data ./data
RUN useradd --create-home desk && mkdir results && chown -R desk /app
USER desk
EXPOSE 8088
HEALTHCHECK --interval=15s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8088/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8088"]
