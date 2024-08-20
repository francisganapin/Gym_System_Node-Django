import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { join, extname } from 'node:path';

const mimeTypes = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
};

const server = createServer(async (req, res) => {
  let filePath;
  if (req.url === '/' || req.url === '/homepage' || req.url === '/homepage.html') {
    filePath = join(process.cwd(), 'homepage.html');
  } else {
    filePath = join(process.cwd(), req.url);
  }

  console.log(`Serving file: ${filePath}`);
  try {
    const content = await readFile(filePath);
    const ext = extname(filePath);
    const mimeType = mimeTypes[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mimeType });
    res.end(content);
  } catch (error) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('File not found');
  }
});

server.listen(3000, '127.0.0.1', () => {
  console.log('Listening on http://127.0.0.1:3000');
});
