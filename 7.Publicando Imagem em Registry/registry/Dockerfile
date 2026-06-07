FROM python:3.13-slim

WORKDIR /app

COPY app.py .

ENV APP_NAME="Aplicação vinda do Docker Hub"
ENV APP_VERSION="1.0"
ENV PORT=8000

EXPOSE 8000

CMD ["python", "app.py"]
