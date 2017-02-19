import http.server

registered_routes = {}
me = ('localhost.localdomain', 8080)
group = [me]

class ReSTHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.server.server_name
        port = self.server.server_port
        path_pieces = self.path.split('/')
        registered_routes['/' + path_pieces[1]]((host, port), path_pieces[2])
        self.send_response(200)
        self.end_headers()

def basic_multicast(g, path, m):
    import requests
    for (host, port) in g:
        r = requests.get('http://%s:%d%s/%s' % (host, port, path, m))

def reliable_multicast(g, path, m):
    basic_multicast(g, path, m)

def reliable_receive(path):
    r = set()
    def real_dec(f):
        def wrapper(sender, m):
            if not m in r:
                r.add(m)
                if me != sender: 
                    basic_multicast(group, path, m)
                f(m)

        registered_routes[path] = wrapper
        return wrapper
    return real_dec


@reliable_receive("/test")
def testaaaa(m):
    print("mensagem entregue a aplicação: %s" % m)


def start_server():
    daemon = http.server.HTTPServer(('localhost', 8080), ReSTHandler)
    daemon.serve_forever()
import threading
t = threading.Thread(target=start_server)
t.start()

print("terminei processamento inicial")

reliable_multicast(group, '/test', "hello")
reliable_multicast(group, '/test', "world")

