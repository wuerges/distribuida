import requests
import bottle
import json
import threading
import time
import sys

lock = threading.Lock()

peers = sys.argv[2:]

@bottle.route('/peers')
def index():
    return json.dumps(peers)

def fault_detector():
    global lock
    time.sleep(5)
    while True:
        time.sleep(1)
        np = set()
        for p in peers:
            try:
                r = requests.get(p + '/peers')
                np.add(p)
            except requests.exceptions.ConnectionError:
                pass
        with lock:
            peers[:] = list(np)


def client():
    global lock
    time.sleep(5)
    while True:
        time.sleep(1)
        np = []
        for p in peers:
            try:
                r = requests.get(p + '/peers')
                np.append(p)
                np.extend(json.loads(r.text))
            except requests.exceptions.ConnectionError:
                pass

            time.sleep(1)
        with lock:
            peers[:] = list(set(np))

        print(peers)

t = threading.Thread(target=client)
t.start()

t2 = threading.Thread(target=fault_detector)
t2.start()

bottle.run(host='localhost', port=int(sys.argv[1]))
