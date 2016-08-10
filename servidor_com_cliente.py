import requests
import bottle
import json
import threading
import time
import sys

peers = sys.argv[2:]

@bottle.route('/peers')
def index():
    return json.dumps(peers)

def client():
    time.sleep(5)
    while True:
        time.sleep(1)
        np = []
        for p in peers:
            r = requests.get(p + '/peers')
            np = np + json.loads(r.text)
            print(np)
            time.sleep(1)
        peers[:] = list(set(np + peers))

        print(peers)

t = threading.Thread(target=client)
t.start()

bottle.run(host='localhost', port=int(sys.argv[1]))
