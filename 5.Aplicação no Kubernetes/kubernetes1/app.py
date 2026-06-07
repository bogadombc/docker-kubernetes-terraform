from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
from datetime import datetime

APP_NAME = os.getenv("APP_NAME", "Aplicação Kubernetes")
APP_VERSION = os.getenv("APP_VERSION", "v1")
PORT = int(os.getenv("PORT", "8000"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = f"""
        <html>
            <head>
                <title>{APP_NAME}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background: #f4f7fb;
                        color: #14213d;
                        padding: 40px;
                    }}
                    .card {{
                        background: white;
                        border-radius: 16px;
                        padding: 32px;
                        max-width: 720px;
                        margin: auto;
                        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
                    }}
                    .version {{
                        display: inline-block;
                        padding: 8px 16px;
                        background: #2563eb;
                        color: white;
                        border-radius: 999px;
                        font-weight: bold;
                    }}
                    code {{
                        background: #eef2ff;
                        padding: 4px 8px;
                        border-radius: 6px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>{APP_NAME}</h1>
                    <p class="version">Versão: {APP_VERSION}</p>
                    <p>Aplicação rodando dentro do Kubernetes.</p>
                    <p><strong>Pod/Hostname:</strong> <code>{hostname}</code></p>
                    <p><strong>Horário da requisição:</strong> {now}</p>
                </div>
            </body>
        </html>
        """

        print(f"Requisição recebida no pod {hostname} - versão {APP_VERSION}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"{APP_NAME} {APP_VERSION} iniciada na porta {PORT}")
server.serve_forever()
