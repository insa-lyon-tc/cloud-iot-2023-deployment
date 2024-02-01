// kafkaConsumer.js
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['kafka.kafka.svc.cluster.local:9092']
});


const consumer = kafka.consumer({ groupId: 'python' });

const imagesByTopic = {};

const topics = [
  'CIT_CAMERA_1', 'CIT_CAMERA_2', 'CIT_CAMERA_3', 'CIT_CAMERA_4', 'CIT_CAMERA_5',
  'CIT_CAMERA_PROCESSED_1', 'CIT_CAMERA_PROCESSED_2', 'CIT_CAMERA_PROCESSED_3', 'CIT_CAMERA_PROCESSED_4', 'CIT_CAMERA_PROCESSED_5'
];
topics.forEach(topic => imagesByTopic[topic] = []);

const run = async () => {
  await consumer.connect();
  await Promise.all(topics.map(topic => consumer.subscribe({ topic, fromBeginning: true })));

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const image = message.value.toString();
      imagesByTopic[topic].unshift(image);
    },
  });
};

run().catch(console.error);

module.exports = imagesByTopic;
