# Coroutines as Tasks
    # Coroutines can be suspended and resumed
    # yield suspends execution
    # send() resumes execution
    # close() terminates execution


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.__next__()
        return cr

    return start