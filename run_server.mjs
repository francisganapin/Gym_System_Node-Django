import { createServer } from 'http';
import { readFile } from 'fs/promises';
import { join, extname } from 'path';

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
  
  } else if (req.url.startsWith('/css') || req.url.startsWith('/scripts') || req.url.startsWith('/images')) {
    filePath = join(process.cwd(), 'project', req.url);



  
  //member link  start 
  } else if (req.url === '/member/list') {
    filePath = join(process.cwd(), 'project/member/list_member.html');

  } else if (req.url === '/member/login') {
    filePath = join(process.cwd(), 'project/member/login_member.html');
  
  } else if (req.url === '/member/register') {
    filePath = join(process.cwd(), 'project/member/register_member.html');

  } else if (req.url === '/member/delete') {
    filePath = join(process.cwd(), 'project/member/delete_member.html');

  } else if (req.url === '/member/update') {
    filePath = join(process.cwd(), 'project/member/update_member.html');
 //member link  end


  //trainor link
  } else if (req.url === '/trainor/list') {
    filePath = join(process.cwd(), 'project/trainor/trainor_list.html');

  } else if (req.url === '/trainor/delete') {
    filePath = join(process.cwd(), 'project/trainor/trainor_delete.html');

  } else if (req.url === '/trainor/register') {
    filePath = join(process.cwd(), 'project/trainor/trainor_register.html');
  //trainor link

   //class link  start 
  } else if (req.url === '/class/list') {
    filePath = join(process.cwd(), 'project/class/class_list.html');

  } else if (req.url === '/class/delete') {
    filePath = join(process.cwd(), 'project/class/delete_class.html');
  
  } else if (req.url === '/class/register') {
    filePath = join(process.cwd(), 'project/class/register_class.html');
  //class link end

  
     //inventory link  start 
  } else if (req.url === '/inventory/list') {
      filePath = join(process.cwd(), 'project/inventory/item_list_inventory.html');
  
  } else if (req.url === '/inventory/delete') {
      filePath = join(process.cwd(), 'project/inventory/delete_inventory.html');
    
  } else if (req.url === '/inventory/update') {
      filePath = join(process.cwd(), 'project/inventory/update_inventory.html');

  } else if (req.url === '/inventory/register') {
      filePath = join(process.cwd(), 'project/inventory/register_inventory.html');
    //inventory link  end

  } else {
    filePath = join(process.cwd(), 'project/404.html');
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
