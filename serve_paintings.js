const http = require('http');
const fs = require('fs');
const path = require('path');

const DIR = path.join(__dirname, 'paintings');
const PORT = 9876;

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.url === '/list') {
    const files = fs.readdirSync(DIR).filter(f => f.endsWith('.jpg')).sort().reverse();
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify(files));
    return;
  }
  
  const file = decodeURIComponent(req.url.slice(1));
  const filePath = path.join(DIR, file);
  
  if (!fs.existsSync(filePath)) {
    res.writeHead(404);
    res.end('not found');
    return;
  }
  
  const data = fs.readFileSync(filePath);
  res.writeHead(200, {'Content-Type': 'image/jpeg', 'Cache-Control': 'max-age=3600'});
  res.end(data);
});

server.listen(PORT, () => {
  console.log('Painting server on http://localhost:' + PORT);
  console.log('List: http://localhost:' + PORT + '/list');
});
