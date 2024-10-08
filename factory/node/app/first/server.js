const express = require('express');
const app = express();
const port = 5003;

app.get('/hi', (req, res) => {
  res.send('Hi! NodeJS');
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running at http://localhost:${port}`);
});
