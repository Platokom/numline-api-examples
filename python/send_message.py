"""Отправка сообщения через API Numline (без сторонних библиотек).

python3 send_message.py --chat 345 --text "Добрый день!"
python3 send_message.py --channel 12 --phone 79990001122 --text "Добрый день!"
"""
import argparse
import json
import os
import urllib.error
import urllib.request

API = "https://app.numline.ru/api/v1"


def call(method, path, payload=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={
            "Authorization": "Bearer " + os.environ["NUMLINE_API_KEY"],
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read() or b"{}")
        raise SystemExit(f"{e.code} {err.get('code')}: {err.get('error')}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--chat", type=int, help="id чата из GET /chats")
    p.add_argument("--channel", type=int, help="id номера из GET /channels")
    p.add_argument("--phone", help="телефон собеседника, 11 цифр")
    p.add_argument("--text", required=True)
    p.add_argument("--author", help="имя сотрудника, как подписать ответ")
    a = p.parse_args()

    if a.chat:
        body = {"chat_id": a.chat}
    elif a.channel and a.phone:
        body = {"channel_id": a.channel, "phone": a.phone}
    else:
        p.error("нужен --chat или --channel вместе с --phone")
    body["text"] = a.text
    if a.author:
        body["author"] = a.author

    msg = call("POST", "/messages", body)
    print(f"сообщение {msg['id']} в чате {msg['chat_id']}, статус {msg['status']}")


if __name__ == "__main__":
    main()
