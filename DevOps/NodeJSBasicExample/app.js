var express = require('express');
app = express.createServer();

var PORT = 80;

app.get('/', function(req, res){
    res.send('Hello world!');
});

app.listen(PORT);
console.log("Server is running on port " + PORT);