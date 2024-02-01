const express = require('express');
const app = express();
const port = 3000;

const imagesByTopic = require('./kafkaConsumer');

app.set('view engine', 'ejs');
app.use(express.static('public'));

app.get('/', (req, res) => {
  res.render('index', { imagesByTopic: {} });
});

app.get('/images', (req, res) => {
  const selectedTopics = req.query.topics ? req.query.topics.split(',') : [];
  const selectedImages = {};

  selectedTopics.forEach(topic => {
    selectedImages[topic] = imagesByTopic[topic] || [];
  });

  res.render('index', { imagesByTopic: selectedImages });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

app.get('/image-count', (req, res) => {
  const counts = Object.fromEntries(
    Object.keys(imagesByTopic).map(topic => [topic, imagesByTopic[topic].length])
  );
  res.json(counts);
});
