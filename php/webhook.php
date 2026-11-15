<?php
// Приём вебхуков Numline с проверкой подписи.
// Положите файл на сервер с https и укажите его адрес в «Настройки» → «API и вебхуки».

$secret = getenv('NUMLINE_WEBHOOK_SECRET');
$body = file_get_contents('php://input');
$signature = $_SERVER['HTTP_X_NUMLINE_SIGNATURE'] ?? '';
$expected = 'sha256=' . hash_hmac('sha256', $body, $secret);

if (!hash_equals($expected, $signature)) {
    http_response_code(401);
    exit;
}

$event = json_decode($body, true);
$data = $event['data'] ?? [];
// Одно событие может прийти дважды: сверяйте $_SERVER['HTTP_X_NUMLINE_DELIVERY'] с уже обработанными.

switch ($event['event']) {
    case 'message.incoming':
        $chat = $data['chat'] ?? [];
        error_log("{$chat['kind']} {$chat['phone']}: {$data['text']}");
        break;
    case 'message.status':
        error_log("сообщение {$data['id']}: {$data['status']}");
        break;
    case 'channel.state':
        error_log("номер {$data['phone']}: {$data['state']}");
        break;
}

http_response_code(200);
