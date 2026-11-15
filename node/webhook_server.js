// Приём вебхуков Numline с проверкой подписи (Node.js 18+, без зависимостей).
// NUMLINE_WEBHOOK_SECRET=whsec_... node webhook_server.js

import { createServer } from 'node:http';
import { createHmac, timingSafeEqual } from 'node:crypto';

const secret = process.env.NUMLINE_WEBHOOK_SECRET;
const seen = new Set(); // id обработанных событий; в рабочем коде храните в базе

function valid(body, signature = '') {
  const expected = Buffer.from('sha256=' + createHmac('sha256', secret).update(body).digest('hex'));
  const got = Buffer.from(signature);
  return got.length === expected.length && timingSafeEqual(got, expected);
}

createServer((req, res) => {
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  req.on('end', () => {
    const body = Buffer.concat(chunks);
    if (!valid(body, req.headers['x-numline-signature'])) {
      res.writeHead(401).end();
      return;
    }
    const delivery = req.headers['x-numline-delivery'];
    if (!seen.has(delivery)) {
      seen.add(delivery);
      const { event, data = {} } = JSON.parse(body);
      if (event === 'message.incoming') {
        console.log(`${data.chat?.kind} ${data.chat?.phone}: ${data.text}`);
      } else if (event === 'message.status') {
        console.log(`сообщение ${data.id}: ${data.status}`);
      } else {
        console.log(event);
      }
    }
    res.writeHead(200).end();
  });
}).listen(8080);
