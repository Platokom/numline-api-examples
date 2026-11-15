"""Приём вебхуков Numline с проверкой подписи (без сторонних библиотек).

NUMLINE_WEBHOOK_SECRET=whsec_... python3 webhook_server.py
Сервер слушает порт 8080; снаружи его нужно открыть по https (nginx, Caddy и т. п.).
"""
import hashlib
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ["NUMLINE_WEBHOOK_SECRET"].encode()
seen = set()  # id обработанных событий; в рабочем коде храните в базе


def valid(body: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature or "")


def handle(event: dict):
    kind = event["event"]
    data = event.get("data") or {}
    if kind == "message.incoming":
        chat = data.get("chat") or {}
        print(f"{chat.get('kind')} {chat.get('phone') or chat.get('username')}: {data.get('text')}")
    elif kind == "message.status":
        print(f"сообщение {data.get('id')}: {data.get('status')} {data.get('error') or ''}")
    elif kind == "channel.state":
        print(f"номер {data.get('phone')}: {data.get('previous')} -> {data.get('state')}")
    else:
        print(kind)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if not valid(body, self.headers.get("X-Numline-Signature")):
            self.send_response(401)
            self.end_headers()
            return
        delivery = self.headers.get("X-Numline-Delivery")
        if delivery not in seen:
            seen.add(delivery)
            handle(json.loads(body))
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
