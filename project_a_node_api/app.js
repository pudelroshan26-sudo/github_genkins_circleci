const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'UP', timestamp: new Date() });
});

app.get('/api/users', (req, res) => {
  res.status(200).json([
    { id: 1, name: 'Roshan Poudel' },
    { id: 2, name: 'Alice Smith' },
    { id: 3, name: 'Bob Jones' }
  ]);
});

app.post('/api/echo', (req, res) => {
  const { message } = req.body;
  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }
  res.status(200).json({ message });
});

if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

module.exports = app;
