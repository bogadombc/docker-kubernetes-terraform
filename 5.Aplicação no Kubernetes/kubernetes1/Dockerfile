FROM python:3.13-slim

WORKDIR /app

COPY app.py .

ENV APP_NAME="Aplicação no Kubernetes"
ENV APP_VERSION="v1"
ENV PORT=8000

EXPOSE 8000

CMD ["python", "app.py"]
