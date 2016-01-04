from bottle import run, get, post, view, request, redirect

messages = ["Hello!"]

@get('/')
@view('index')
def index():
    return {'m': messages}


@post('/send')
def sendMessage():
    m = request.forms.get('message')
    messages.append(m)
    redirect('/')


run(host='localhost', port=8080)
