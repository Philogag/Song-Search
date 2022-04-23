from backend.factory import message_queue


def run_train():
    message_queue.push_task(channel="jiayan+word2vec+cos", method='train', data={})
    return 'Running.'
