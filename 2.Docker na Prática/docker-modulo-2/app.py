from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
from datetime import datetime

APP_NAME = os.getenv("APP_NAME", "Minha aplicação Docker")
PORT = int(os.getenv("PORT", "8000"))
DATA_DIR = "/data"
LOG_FILE = f"{DATA_DIR}/access.log"

os.makedirs(DATA_DIR, exist_ok=True)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostname = socket.gethostname()

        log_message = f"{now} - Acesso recebido no container {hostname}\n"

        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_message)

        response = f"""
        <html>
            <head>
                <title>{APP_NAME}</title>
            </head>
            <body>
                <h1>{APP_NAME}</h1>
                <p>Aplicação rodando dentro de um container Docker.</p>
                <p>Hostname do container: {hostname}</p>
                <p>Porta interna da aplicação: {PORT}</p>
                <p>Log gravado em: {LOG_FILE}</p>
            </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"{APP_NAME} iniciada na porta {PORT}")
server.serve_forever()