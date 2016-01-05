from bottle import run, get, put
import json


def subkeys(k):
    for i in range(len(k), 0, -1):
        yield k[:i]
    yield ""


class DHT:
    def __init__(self, h):
        self.k = h
        self.h = {}

        for sk in subkeys(self.k):
            self.h[sk] = None

    def insert(self, k, v):
        for sk in subkeys(k):
            if sk in self.h:
                if not self.h[sk]:
                    self.h[sk] = (k, v)
                    return sk
        return None

    def lookup(self, k):
        for sk in subkeys(k):
            if sk in self.h:
                (ki, vi) = self.h[sk]
                if ki == k:
                    return vi
        return None

    def __repr__(self):
        return "<<DHT:"+ repr(self.h) +">>"

dht = DHT("abcd")

@get('/dht/<key>')
def dht_lookup(key):
    global dht
    return json.dumps(dht.lookup(key))

@put('/dht/<key>/<value>')
def dht_insert(key, value):
    global dht
    print(value)
    return json.dumps(dht.insert(key, value))


run(host='localhost', port=8080)
