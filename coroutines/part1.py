import time


def countdown(n):
    print
    "Counting down from", n
    while n > 0:
        yield n
        n -= 1


# demo of countdown
# x = countdown(10)
# for i in x:
#     print(i)

def follow(path):
    thefile = open(path)
    print("following " + path)
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


# Demo of follow (unix tail -f)
# for line in follow("/var/log/syslog"):
#     print(line)

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line


# Demo of grep (example of generator pipeline)
# for line in grep("mudassir kernel", follow("/var/log/syslog")):
#     print("mudassir kernel HAS COME\t" + line)


def grep_yield_as_expr(pattern):
    print("looking for " + pattern)
    try:
        while True:
            line = (yield)
            if pattern in line:
                print("pattern detected in line\t" + line)
    except GeneratorExit:
        print("F**k of I'm going...")


# # demo of yield as expression
# g = grep_yield_as_expr("mudassir")
# g.__next__()
#
# g.send("mudassir wants peace")
# g.send("life screwes")
# g.send("I'm done")
# g.throw("exceptionsssssssssss")


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.__next__()
        return cr

    return start

@coroutine
def grep_yield_as_expr_v2(pattern):
    print("looking for " + pattern)
    while True:
        line = (yield)
        if pattern in line:
            print("pattern detected in line\t" + line)


# demo of using decorator
# g = grep_yield_as_expr_v2("mudassir")
# # This time no need to prime the generator as it is decorated to get primed already
# g.send("mudassir wants peace")
# g.send("life screws")
# g.send("f**k off")
# g.close()
