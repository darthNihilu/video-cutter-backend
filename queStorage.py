import queue

que = queue.Queue()


def storeInQueue(f):
    def wrapper(*args):
        que.put(f(*args))

    return wrapper
