########################### Coroutines and Event Dispatching #######################################

import xml
from xml.sax import ContentHandler


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.__next__()
        return cr

    return start


class EventHandler(ContentHandler):

    def __init__(self, target):
        self.target = target

    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs._attrs)))

    def characters(self, content):
        self.target.send(('text', content))

    def endElement(self, name):
        self.target.send(('end', name))


@coroutine
def buses_to_dict(target):
    while True:
        event, value = (yield)
        # Look for the start of a <bus> element

        if event == 'start' and value[0] == 'bus':
            busdict = {}
            fragment = []

            # Capture text of inner elements in a dict
            while True:
                event, value = (yield)
                if event == 'start':
                    fragment = []
                elif event == 'text':
                    fragment.append(value)
                elif event == 'end':
                    if value != 'bus':
                        busdict[value] = "".join(fragment)
                    else:
                        target.send(busdict)
                        break


@coroutine
def filter_on_field(fieldname, value, target):
    while True:
        d = (yield)
        if d.get(fieldname) == value:
            target.send(d)


@coroutine
def bus_locations():
    while True:
        bus = (yield)
        print(bus)


# filter_on_field("route", "22", target)
# filter_on_field("direction", "North Bound", target)

obj = xml.sax.parse("allroutes.xml",
              EventHandler(
                  buses_to_dict(
                      filter_on_field("route", "147",
                                      filter_on_field("direction", "North Bound",
                                                      bus_locations())))
              ))

print(obj)
