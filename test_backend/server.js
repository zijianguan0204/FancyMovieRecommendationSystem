const http = require('http');

const port = process.env.PORT || 5000;
const app = require('./app');
server = http.createServer(app);

console.log('Server Start');

server.listen(port);