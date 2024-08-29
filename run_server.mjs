import { createServer } from 'http';
import { readFile } from 'fs/promises';  // Importing from 'fs/promises'
import { join, extname } from 'path';  // Using ES module syntax for 'path'

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  // Add more MIME types as needed
};

const server = createServer(async (req, res) => {
  let filePath;
  if (req.url === '/' || req.url === '/homepage' || req.url === '/homepage.html') {
    filePath = join(process.cwd(), 'project/homepage.html');

    //member page start
  } else if (req.url === '/member/login') {
    filePath = join(process.cwd(), 'project/member/login_member.html');
  
  } else if (req.url === '/member/register') {
    filePath = join(process.cwd(), 'project/member/register_member.html');
  
  } else if (req.url === '/member/delete') {
    filePath = join(process.cwd(), 'project/member/delete_member.html');

  } else if (req.url === '/member/update') {
    filePath = join(process.cwd(), 'project/member/update_member.html');
    //member page end

  } else if (req.url === '/trainor') {
    filePath = join(process.cwd(), 'proejct/trainor/trainor.html');
  } else if (req.url === '/trainor/delete') {
    

    filePath = join(process.cwd(), 'proejct/trainor/trainor_delete.html');
  } else if (req.url === '/trainor/register') {


    filePath = join(process.cwd(), 'proejct/trainor/trainor_register.html');
  } else if (req.url === '/register_class') {


      filePath = join(process.cwd(), 'register_class.html');

  } else {

    filePath = join(process.cwd(), '404.html'); 
  }

  console.log(`Serving file: ${filePath}`);
  try {
    const content = await readFile(filePath);
    const ext = extname(filePath);
    const mimeType = mimeTypes[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mimeType });
    res.end(content);
  } catch (error) {
    console.error(`Error serving file: ${error.message}`);
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('File not found');
  }
});


server.listen(3000, '127.0.0.1', () => {
  console.log('Listening on http://127.0.0.1:3000');
});

