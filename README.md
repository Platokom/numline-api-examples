# Примеры API Numline

Короткие примеры для [API Numline](https://numline.ru/api): отправка сообщений в WhatsApp, Telegram и MAX и приём входящих через вебхуки с проверкой подписи. Пригодятся, если вы подключаете мессенджеры к своей CRM, сайту или n8n, Make и Albato.

Numline подключает WhatsApp, Telegram, MAX, Авито и SMS к amoCRM, Битрикс24 и другим системам через API. Полная документация: https://numline.ru/api

## Что внутри

| Папка | Отправка сообщения | Приём вебхука |
| --- | --- | --- |
| `python/` | `send_message.py` | `webhook_server.py` |
| `php/` | `send_message.php` | `webhook.php` |
| `node/` | `send_message.js` | `webhook_server.js` |

Примеры без сторонних библиотек: Python 3.8+, PHP 7.4+ с curl, Node.js 18+.

## Перед началом

1. Создайте ключ в личном кабинете: «Настройки» → «API и вебхуки» → «Создать ключ». Ключ показывается один раз.
2. Для вебхуков добавьте там же адрес вашего сервера (только https) и скопируйте секрет `whsec_...`.
3. Передайте ключ и секрет через переменные окружения:

```
export NUMLINE_API_KEY=nl_ваш_ключ
export NUMLINE_WEBHOOK_SECRET=whsec_ваш_секрет
```

## Отправка

```
python3 python/send_message.py --chat 345 --text "Добрый день! Заказ готов"
python3 python/send_message.py --channel 12 --phone 79990001122 --text "Добрый день!"
```

Номера компании (`channel_id`) отдаёт `GET /channels`, чаты - `GET /chats`. В ответ на отправку приходит созданное сообщение, окончательный статус (`delivered`, `read`, `failed`) - вебхуком `message.status`.

## Вебхуки

Numline присылает POST с JSON и заголовками:

- `X-Numline-Event` - событие: `message.incoming`, `message.outgoing`, `message.status`, `channel.state`, `webhook.test`;
- `X-Numline-Delivery` - id события, одно событие может прийти дважды;
- `X-Numline-Signature` - `sha256=` и HMAC-SHA256 сырого тела запроса с секретом вебхука.

Сервер должен ответить кодом 2xx за 10 секунд, иначе доставка повторится через 1, 5 и 30 минут, 2, 6 и 12 часов. Подпись считается по телу запроса как есть, до разбора JSON.

## Ограничения

120 запросов в минуту на ключ, 30 отправок в минуту с номера, не больше одного нового собеседника в минуту с номера. Мессенджеры блокируют номера за массовые сообщения незнакомым людям, поэтому API не подходит для рассылок.

## Вопросы

support@numline.ru или чат в личном кабинете https://app.numline.ru

Лицензия MIT.
