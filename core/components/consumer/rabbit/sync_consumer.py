import pika
from core.config import config
from core.models.messages.queue import QueueMessage
from core.components.consumer.base_consumer import BaseConsumer
import json


class SyncConsumer(BaseConsumer):
    def __init__(self, queue_name: str):
        self._parameters = pika.ConnectionParameters(
            host=config.RabbitMQConfig.url,
            port=config.RabbitMQConfig.port,
            credentials=pika.PlainCredentials(
                username=config.RabbitMQConfig.login,
                password=config.RabbitMQConfig.password,
            ),
        )
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue_name)
        self._channel.basic_consume(queue_name, self._processing_message, auto_ack=True)

    def _processing_message(self, channel, method_frame, header_frame, body) -> QueueMessage:
        return QueueMessage(**json.loads(body))

    def wait_new_messages(self) -> None:
        while True:
            try:
                self._channel.start_consuming()
            except:
                self._channel.stop_consuming()
                raise


if __name__ == '__main__':
    cons = SyncConsumer(queue_name=config.RabbitMQConfig.web2loader_queue_name)
    cons.wait_new_messages()
