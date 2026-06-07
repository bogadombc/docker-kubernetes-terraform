from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
from datetime import datetime

APP_NAME = os.getenv("APP_NAME", "Aplicação vinda do Registry")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
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
                        background: #f8fafc;
                        color: #0f172a;
                        padding: 40px;
                    }}
                    .card {{
                        background: white;
                        max-width: 760px;
                        margin: auto;
                        padding: 32px;
                        border-radius: 18px;
                        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
                    }}
                    .badge {{
                        display: inline-block;
                        background: #2563eb;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 999px;
                        font-weight: bold;
                    }}
                    code {{
                        background: #e2e8f0;
                        padding: 4px 8px;
                        border-radius: 6px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="badge">Docker Registry</div>
                    <h1>{APP_NAME}</h1>
                    <p><strong>Versão:</strong> {APP_VERSION}</p>
                    <p>Esta aplicação foi executada a partir de uma imagem publicada em um registry.</p>
                    <p><strong>Container/Hostname:</strong> <code>{hostname}</code></p>
                    <p><strong>Horário:</strong> {now}</p>
                </div>
            </body>
        </html>
        """

        print(f"Requisição recebida no container {hostname}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"{APP_NAME} iniciada na porta {PORT}")
server.serve_forever()
