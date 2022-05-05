import json
import logging
from functools import wraps
from typing import Callable

import pika


def get_method_name_key(channel: str, method: str) -> str:
    return "{0}_{1}".format(channel.lower(), method.lower())


class MessageQueue:
    def __init__(self, rabbit_mq_conn_str: str = None):
        # print(rabbit_mq_conn_str)
        if rabbit_mq_conn_str:
            parameters = pika.URLParameters(rabbit_mq_conn_str)
            parameters.heartbeat = 0
            self.conn = pika.BlockingConnection(parameters)
            self.channel = self.conn.channel()

    def push_task(self, channel: str, method: str, data: any):
        queue_name = get_method_name_key(channel, method)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(data).encode(),
        )

    def start_listen(self):
        self.channel.start_consuming()

    def register_listener(self, channel: str, method: str, callback: Callable):
        queue_name = get_method_name_key(channel, method)
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,  # data_unpack then call the real func
            auto_ack=False,
        )

    @classmethod
    def data_unpacker(cls) -> Callable:
        def __actual_data_unpacker(func: Callable):
            @wraps(func)
            def wrapper(ch, method, properties, body):
                try:
                    data = json.loads(body.decode())
                    logging.info(f'Message data: {data}')
                    if isinstance(data, dict):
                        func(**data)
                    else:
                        func(data)
                    ch.basic_ack(method.delivery_tag)
                except Exception as e:
                    logging.exception(e)
                    # ch.basic_nack(method.delivery_tag)
            return wrapper

        return __actual_data_unpacker
