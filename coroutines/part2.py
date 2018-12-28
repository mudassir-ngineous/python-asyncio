import time


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.__next__()
        return cr

    return start


def follow(thefile, target):
    thefile.seek(0, 2)  # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line and line != "":
            time.sleep(0.1)  # Sleep briefly
            continue
        target.send(line)


@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


# f = open("/var/log/syslog")
# follow(f, printer())


@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


#
# f = open("/home/mudassir/impdata.json")
# print(f.readlines())
# follow(f,
#        grep("kernel",
#             printer()))


@coroutine
def broadcast(targets):
    while True:
        item = (yield)
        for t in targets:
            t.send(item)


# # testing broadcase using generator & coroutine
# f = open("/home/mudassir/impdata.json")
# follow(f, broadcast([
#     grep("python", printer()),
#     grep("mudassir", printer()),
#     grep("python", printer())
# ]))

class GrepHandler(object):
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target

    def send(self, line):
        if self.pattern in line:
            self.target.send(line)


@coroutine
def null():
    while True:
        item = (yield)


line = "python is good"
p1 = grep('python', null())
p2 = GrepHandler('python', null())

# the speed of output by p1 & p2 can be tested by sending 10000000 lines to them, p1's behavior will be faster than p2's

# primary reason being coroutines are 'self'-free

