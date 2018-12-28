# From Data Processing to Concurrent Programming
import pickle


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.__next__()
        return cr

    return start


## sample codes kind of pseudo code, can't be run due to unfulfilled dependencies
@coroutine
def threaded(target):
    messsages = Queue()

    def run_target():
        while True:
            item = messages.get()

            if item is GeneratorExit:
                target.close()
                return
            else:
                target.send(item)

    Thread(target=run_target()).start()

    try:
        while True:
            item = (yield)
            messsages.put(item)
    except GeneratorExit:
        messsages.put(GeneratorExit)


@coroutine
def sendto(f):
    try:
        while True:
            item = (yield)
            pickle.dump(item, f)
            f.flush()
    except StopIteration:
        f.close()


def recvfrom(f, target):
    try:
        while True:
            item = pickle.load(f)
            target.send(item)
    except EOFError:
        target.close()
