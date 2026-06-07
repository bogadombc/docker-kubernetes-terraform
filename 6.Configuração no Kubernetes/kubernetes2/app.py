from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
from datetime import datetime

APP_NAME = os.getenv("APP_NAME", "Aplicação sem configuração")
APP_ENV = os.getenv("APP_ENV", "local")
APP_VERSION = os.getenv("APP_VERSION", "v1")
SYSTEM_USER = os.getenv("SYSTEM_USER", "usuario-nao-definido")
SYSTEM_PASSWORD = os.getenv("SYSTEM_PASSWORD", "senha-nao-definida")
PORT = int(os.getenv("PORT", "8000"))

MESSAGE_FILE = "/config/mensagem.txt"
LOG_FILE = "/data/access.log"


def read_message_file():
    try:
        with open(MESSAGE_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Não foi possível ler o arquivo de configuração: {e}"


def mask_password(password):
    if not password:
        return "não definida"

    if len(password) <= 2:
        return "*" * len(password)

    return password[0] + "*" * (len(password) - 2) + password[-1]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = read_message_file()

        os.makedirs("/data", exist_ok=True)

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{now} - Requisição recebida no pod {hostname}\n")

        response = f"""
        <html>
            <head>
                <title>{APP_NAME}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background: #f8fafc;
                        color: #0f172a;
                        padding: 40px;
                    }}
                    .card {{
                        background: white;
                        border-radius: 18px;
                        padding: 32px;
                        max-width: 820px;
                        margin: auto;
                        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
                    }}
                    .badge {{
                        display: inline-block;
                        padding: 8px 14px;
                        border-radius: 999px;
                        background: #2563eb;
                        color: white;
                        font-weight: bold;
                        margin-bottom: 16px;
                    }}
                    .section {{
                        border-top: 1px solid #e2e8f0;
                        padding-top: 18px;
                        margin-top: 18px;
                    }}
                    code {{
                        background: #e2e8f0;
                        padding: 4px 8px;
                        border-radius: 6px;
                    }}
                    .secret {{
                        color: #b91c1c;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="badge">Kubernetes Configuração</div>

                    <h1>{APP_NAME}</h1>
                    <p><strong>Ambiente:</strong> {APP_ENV}</p>
                    <p><strong>Versão:</strong> {APP_VERSION}</p>

                    <div class="section">
                        <h2>ConfigMap como arquivo</h2>
                        <p>{message}</p>
                        <p><strong>Arquivo lido:</strong> <code>{MESSAGE_FILE}</code></p>
                    </div>

                    <div class="section">
                        <h2>Secret como variável de ambiente</h2>
                        <p><strong>Usuário:</strong> {SYSTEM_USER}</p>
                        <p><strong>Senha:</strong> <span class="secret">{mask_password(SYSTEM_PASSWORD)}</span></p>
                    </div>

                    <div class="section">
                        <h2>Informações do Pod</h2>
                        <p><strong>Pod/Hostname:</strong> <code>{hostname}</code></p>
                        <p><strong>Horário:</strong> {now}</p>
                        <p><strong>Log gravado em:</strong> <code>{LOG_FILE}</code></p>
                    </div>
                </div>
            </body>
        </html>
        """

        print(f"Requisição recebida no pod {hostname}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"{APP_NAME} iniciada na porta {PORT}")
server.serve_forever()