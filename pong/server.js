#!/usr/bin/env node

const http = require('http');
const fs   = require('fs');
const path = require('path');

const port = 3000;
const srv  = http.createServer((req, res) => {
  if (req.url === '/') {
    fs.readFile(path.join(__dirname, 'index.html'), (err, data) => {
      if (err) {
        res.writeHead(500, {'Content-Type': 'text/plain'});
        return res.end('Server error reading index.html');
      }
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(data);
    });
  } else {
    res.writeHead(404, {'Content-Type': 'text/plain'});
    res.end('Not Found');
  }
});

srv.listen(port, () => {
  console.log(`HTTP server running at http://localhost:${port}`);
});

