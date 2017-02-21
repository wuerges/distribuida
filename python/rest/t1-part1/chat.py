from bottle import run, get, post, view, request, redirect

messages = [("Nobody", "Hello!")]
nick = "Nobody"

@get('/')
@view('index')
def index():
    return {'messages': messages, 'nick': nick}


@post('/send')
def sendMessage():
    global nick
    m = request.forms.get('message')
    n = request.forms.get('nick')
    messages.append([n, m])
    nick = n
    redirect('/')


run(host='localhost', port=8080)
