import os
import sys

root = os.path.dirname(__file__) + "/../"  # 定位到project根目录
sys.path.append(root)

from backend.app_entry import flask_app
from backend.factory import message_queue

from backend.algorithm.model1.word2vec import message_queue_register

if __name__ == '__main__':
    total_register = [
        *message_queue_register
    ]

    message_queue.start_listen()
