from core.components.producer.base_producer import BaseSyncProducer
import pika
from core.config import config
from core.models.messages.queue import QueueMessage
from datetime import datetime


class SyncRabbitProducer(BaseSyncProducer):
    def __init__(self, queue_name: str, exchange: str = ''):
        self._parameters = pika.ConnectionParameters(
            host=config.RabbitMQConfig.url,
            port=config.RabbitMQConfig.port,
            credentials=pika.PlainCredentials(
                username=config.RabbitMQConfig.login,
                password=config.RabbitMQConfig.password,
            ),
            blocked_connection_timeout=config.RabbitMQConfig.timeout,
        )
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue_name)
        self._queue_name = queue_name

    def send(self, message: QueueMessage) -> None:
        self._channel.basic_publish(exchange='', routing_key=self._queue_name, body=message.json())
        self._connection.close()


if __name__ == '__main__':
    prod = SyncRabbitProducer(queue_name=config.RabbitMQConfig.web2loader_queue_name)
    msg = QueueMessage(id=datetime.utcnow().timestamp(), data={})
    prod.send(msg)
