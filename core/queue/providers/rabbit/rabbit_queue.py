import pika
import json
from typing import Optional, Callable

from core.queue.base.base_queue import BaseQueue, AsyncBaseQueue
from core.models.messages.queue import PopResult, PushResult, QueueMessage
from core.config import config


def on_message_callback(ch, method, properties, body):
    print(body)


class RabbitQueue(BaseQueue):
    _credentials = pika.PlainCredentials(config.RabbitMQConfig.login, config.RabbitMQConfig.password)
    _config = pika.ConnectionParameters(
        host=config.RabbitMQConfig.url,
        port=config.RabbitMQConfig.port,
        credentials=_credentials,
    )

    def __init__(self, queue_name: str):
        self._connection = pika.BlockingConnection(self._config)
        self._channel = self._connection.channel()
        self._queue_name: str = queue_name

    def pop(self) -> PopResult:
        self._channel.queue_declare(self._queue_name)
        self._channel.basic_consume(queue=self._queue_name, auto_ack=True, on_message_callback=on_message_callback)
        self._channel.start_consuming()

    def push(self, message: QueueMessage) -> PushResult:
        self._channel.queue_declare(self._queue_name)
        self._channel.basic_publish(exchange='', routing_key=self._queue_name, body=message.json())


if __name__ == '__main__':
    queue = RabbitQueue(queue_name=config.RabbitMQConfig.web2loader_queue_name)
    queue.push(message=QueueMessage(id=1, data={}))
    queue.pop()