// Отправка сообщения через API Numline (Node.js 18+, встроенный fetch).
// NUMLINE_API_KEY=nl_... node send_message.js 345 "Добрый день!"

const [chatId, text] = process.argv.slice(2);
if (!process.env.NUMLINE_API_KEY || !chatId || !text) {
  console.error('Использование: NUMLINE_API_KEY=nl_... node send_message.js <chat_id> <текст>');
  process.exit(1);
}

const res = await fetch('https://app.numline.ru/api/v1/messages', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.NUMLINE_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ chat_id: Number(chatId), text }),
});
const data = await res.json();
if (res.status !== 201) {
  console.error(`Ошибка ${res.status}: ${data.code} ${data.error}`);
  process.exit(1);
}
console.log(`сообщение ${data.id} в чате ${data.chat_id}, статус ${data.status}`);
