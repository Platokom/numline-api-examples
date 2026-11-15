<?php
// Отправка сообщения через API Numline.
// php send_message.php 345 "Добрый день!"

$key = getenv('NUMLINE_API_KEY');
$chatId = (int)($argv[1] ?? 0);
$text = $argv[2] ?? '';
if (!$key || !$chatId || $text === '') {
    exit("Использование: NUMLINE_API_KEY=nl_... php send_message.php <chat_id> <текст>\n");
}

$ch = curl_init('https://app.numline.ru/api/v1/messages');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_HTTPHEADER => [
        'Authorization: Bearer ' . $key,
        'Content-Type: application/json',
    ],
    CURLOPT_POSTFIELDS => json_encode(['chat_id' => $chatId, 'text' => $text], JSON_UNESCAPED_UNICODE),
]);
$body = curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

$data = json_decode($body, true);
if ($code !== 201) {
    exit("Ошибка $code: " . ($data['code'] ?? '') . ' ' . ($data['error'] ?? $body) . "\n");
}
echo "сообщение {$data['id']} в чате {$data['chat_id']}, статус {$data['status']}\n";
